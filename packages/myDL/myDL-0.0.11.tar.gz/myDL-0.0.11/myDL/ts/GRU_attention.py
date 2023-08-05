# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:38:23 2018

@author: jimmybow
"""

import torch
import torch.utils.data as Data
from torch import nn
import torch.nn.functional as F
import random
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from mydf import *
from datetime import datetime, timedelta
import math
import copy
import pkg_resources
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pandas.plotting import register_matplotlib_converters
import io
import imageio

###############################################################################################################
###  define class
###############################################################################################################
class torch_Dataset(Data.Dataset): # 需要继承 data.Dataset
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __getitem__(self, index):
        data = (self.x[index], self.y[index])
        return data
    def __len__(self):
        return len(self.y)

class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, max_length):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.max_length = max_length

        self.attn = nn.Linear(2*self.hidden_size, self.max_length) # 512 => 10
        self.attn_combine = nn.Linear(2*self.hidden_size, self.hidden_size) # 512 => 256
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)

    def forward(self, input, hidden, encoder_last_layer_outputs):
        attn = self.attn(torch.cat((input[0], hidden[0]), 1)) # (1, 2*hidden_size) => (1, max_length)
        attn_weights = F.softmax(attn, dim=1)                    # (1, max_length)
        # (1, 1, max_length) X (1, max_length, hidden_size) = (1, 1, hidden_size)  encoder_last_layer_outputs 的線性組合
        attn_applied = torch.bmm(attn_weights.unsqueeze(0), encoder_last_layer_outputs.unsqueeze(0))  # (1, 1, hidden_size)

        output = torch.cat((input[0], attn_applied[0]), 1)    # (1, 2*hidden_size)
        output = self.attn_combine(output).unsqueeze(0)          # (1, 1, hidden_size)

        output = F.relu(output)                                  # (1, 1, hidden_size)
        output, hidden = self.gru(output, hidden)
        return output, hidden      # (1, 1, hidden_size), (1, 1, hidden_size)

class GRU_seq2seq(nn.Module):
    def __init__(self, input_size=5, hidden_size=10, output_size=3, prediction_length=12, time_step=24):
        super(GRU_seq2seq, self).__init__()
        
        self.prediction_length = prediction_length
        self.GRU_encoder = nn.GRU(input_size, hidden_size, batch_first=True)
        self.GRU_decoder = AttnDecoderRNN(hidden_size, max_length=time_step)
        self.reg = nn.Linear(hidden_size, output_size) 
      
    def forward(self, x):
        x, decoder_hidden = self.GRU_encoder(x) 
        encoder_last_layer_outputs = x[0]
        decoder_input = decoder_hidden  # (1, 1, hidden_size)
        decoder_output_list = []
        for di in range(self.prediction_length):
            decoder_output, decoder_hidden = self.GRU_decoder(decoder_input, decoder_hidden, encoder_last_layer_outputs)
            decoder_output_list.append(decoder_output)
            decoder_input = decoder_output

        output = torch.cat(decoder_output_list, 1)      # (1, prediction_length, hidden_size)
        output = self.reg(output)                       # (1, prediction_length, 3)
        return output

class QuantileLoss(nn.Module):
    def __init__(self, quantiles):
        super().__init__()
        self.quantiles = quantiles
        
    def forward(self, preds, target):
        assert not target.requires_grad
        assert preds.size(0) == target.size(0)
        losses = []
        for i, q in enumerate(self.quantiles):
            errors = target - preds[:, :, i]
            losses.append(
                torch.max( (q-1) * errors, q * errors ).unsqueeze(2)
            )
        loss = torch.mean(torch.sum(torch.cat(losses, dim=2), dim=2))
        return loss
###############################################################################################################
###  define function
###############################################################################################################
def RMSE(x, y, model, std_target, scaler):
    predict_value = [model(x[[i]])[0, :, 0].data.numpy() for i in range(len(x))]
    actual_value =  y.data.numpy()
    return np.sqrt(mean_squared_error(predict_value, actual_value))*std_target*scaler    
    
def fit(data_source, target_column, output_filename = None, model_source = None,
                        freq = '1M',
                        data_use_length = None,
                        prediction_length = 12,
                        time_step = 24,
                        prediction_quantile = [0.05, 0.95],
                        train_set_percent = 0.7,
                        test_set_percent = None,
                        split_way = 'random',
                        hidden_size = 10,
                        learning_rate = 1e-2,
                        weight_decay = 0,
                        early_stopping_patience = 500,
                        epochs = 5000):
    ###############################################################################################################
    ###  preprocessing data
    ###############################################################################################################
    Quantile = [0.5] + prediction_quantile
    mini_batch_size = 1
    
    if isinstance(data_source, str):
        df = pd.read_csv(open(data_source))
    else:
        df = data_source

    if model_source is not None:
        if isinstance(model_source, str): 
            try:    model = torch.load(model_source)
            except: pass    
        else: 
            model = model_source
        
    if 'time' in df.columns.tolist():
        df.index = df.time.astype('datetime64[ns]')
        df >>= drop('time')

    df = df.astype(float).resample(freq).mean()
    if data_use_length is not None: df = df.iloc[-data_use_length:]
    features = df.columns.tolist()
    target_column_index = features.index(target_column)
    time_index = df.index
    if df.isnull().values.sum() > 0:
        print("The data source has missing value after aggregated by freq = '{}'".format(freq))
        print("Filling missing value use method = 'pad'")
        df = df.fillna(method = 'pad').dropna()
    elif len(df) <= time_step + prediction_length - 1:
        raise Exception("The sample size is too low after aggregated, it's not enough to training")
        
    scaler = 10
    scaler_std = preprocessing.StandardScaler()
    data_norm = scaler_std.fit_transform(df)/scaler
    
    # 只會有 len(data_norm) - time_step + 1 個樣本 = len(sample_ranges_x)
    sample_ranges_x = [range(i, i + time_step) for i in range(len(data_norm)) if i + time_step <= len(data_norm)]
    data_x = torch.tensor([data_norm[sample_range] for sample_range in sample_ranges_x]).float()

    # 只會有 len(data_norm) - prediction_length + 1 個樣本 = len(sample_ranges_y)
    sample_ranges_y = [range(i, i + prediction_length) for i in range(len(data_norm)) if i + prediction_length <= len(data_norm)]
    data_y = torch.tensor([data_norm[sample_range, target_column_index] for sample_range in sample_ranges_y]).float()
    
    # 最終只會有 len(sample_ranges_x) - prediction_length = len(sample_ranges_y) - time_step 個學習樣本
    data_x = data_x[:-prediction_length]
    data_y = data_y[time_step:]
    final_ranges_x = sample_ranges_x[:-prediction_length]
    final_ranges_y = sample_ranges_y[time_step:]
    ###############################################################################################################
    ###  apply window-move size = prediction_length/3
    ###############################################################################################################
    #window_move = math.ceil(prediction_length/3)
    #data_x = data_x[::window_move]
    #data_y = data_y[::window_move]
    ###############################################################################################################
    ###  split data to train / validate / test set
    ###############################################################################################################
    if test_set_percent is not None:
        test_size = int(len(data_x) * test_set_percent)
    else:
        test_size = 0
    train_size = int(len(data_x) * train_set_percent)
    validate_size = len(data_x) - train_size - test_size

    if validate_size <= 0: 
        raise Exception('The train_set_percent is too large so that there is no validate set')

    if test_set_percent is not None:
        test_x = data_x[-test_size:]
        test_y = data_y[-test_size:] 
        data_x = data_x[:-test_size]    
        data_y = data_y[:-test_size]

    if split_way == 'random':
        dataset = torch_Dataset(data_x, data_y)
        train_dataset, validate_dataset = Data.random_split(dataset, [train_size, validate_size])
        validate_x = validate_dataset[:][0]
        validate_y = validate_dataset[:][1]
    else:
        train_dataset = torch_Dataset(data_x[:train_size], data_y[:train_size])
        validate_x = data_x[train_size:]
        validate_y = data_y[train_size:] 

    train_x = train_dataset[:][0]
    train_y = train_dataset[:][1]
    ###############################################################################################################
    ###  model train
    ###############################################################################################################
    net = GRU_seq2seq(input_size = len(features),
                      output_size = len(Quantile),
                      hidden_size = hidden_size,
                      time_step = time_step,
                      prediction_length = prediction_length)

    try:     net.load_state_dict(model['state_dict'])
    except:  pass

    train_loader = Data.DataLoader(dataset = train_dataset, batch_size = mini_batch_size, shuffle = True)
    loss_func = QuantileLoss(Quantile)
    optimizer = torch.optim.Adam(net.parameters(), lr = learning_rate, weight_decay = weight_decay)
    
    std_target =  np.sqrt(scaler_std.var_)[target_column_index]
    if std_target == 0: std_target = 1
    
    for epoch in range(epochs):
        # training mode
        net.train()     
        for step, (x, y) in enumerate(train_loader, 1): 
            # 前向传播
            out = net(x)  # (mini_batch, 12, 3)
            loss = loss_func(out, y)  
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        # evaluation mode
        net.eval()        
        validate_RMSE = RMSE(validate_x, validate_y, net, std_target, scaler)
        if epoch == 0 or validate_RMSE < best_validate_RMSE:            
            best_validate_RMSE = validate_RMSE
            best_state_dict = copy.deepcopy(net.state_dict())
            best_epoch = epoch
            print('Best Epoch:', epoch, 'Train_loss:', '%.10f' % loss.item(), 'Validate_RMSE:', '%.10f' % validate_RMSE)
        elif epoch - best_epoch > early_stopping_patience: 
            print("Validate_RMSE don't imporved for {} epoch, training stop !".format(early_stopping_patience))
            break
        else:
            print('     Epoch:', epoch, 'Train_loss:', '%.10f' % loss.item(), 'Validate_RMSE:', '%.10f' % validate_RMSE)
        
    ######################################################################################################
    ###  final model evaluation
    ######################################################################################################
    net.load_state_dict(best_state_dict)
    net.eval()        
    RMSE_train    = RMSE(train_x, train_y, net, std_target, scaler)
    RMSE_validate = RMSE(validate_x, validate_y, net, std_target, scaler)
    RMSE_test     = RMSE(test_x, test_y, net, std_target, scaler)
    print('training complete ! Select Best Epoch:', best_epoch)
    print('train set     RMSE =', RMSE_train)
    print('validate set  RMSE =', RMSE_validate)
    print('test set      RMSE =', RMSE_test)
    ###############################################################################################################
    ###  Output 
    ###############################################################################################################
    output_model = {'state_dict': best_state_dict,
                    'scaler_std':scaler_std,
                    'features': features,
                    'target_column':target_column,
                    'freq': freq,
                    'hidden_size': hidden_size,
                    'Quantile': Quantile,
                    'mini_batch_size': mini_batch_size,
                    'learning_rate': learning_rate,
                    'early_stopping_patience': early_stopping_patience,
                    'epochs': epochs,
                    'best_epoch': best_epoch,
                    'time_step': time_step,
                    'prediction_length': prediction_length,
                    'RMSE_train': RMSE_train,
                    'RMSE_validate': RMSE_validate,
                    'RMSE_test':RMSE_test,
                    'split_way':split_way,
                    'train_size':train_size,
                    'validate_size':validate_size,
                    'test_size':test_size,
                    'train_set_percent':train_set_percent,
                    'test_set_percent':test_set_percent,
                    'weight_decay':weight_decay
                    }
    
    if output_filename is not None: torch.save(output_model, output_filename)
    return output_model
    ###############################################################################################################
    ###  End
    ###############################################################################################################

def predict(data_source, model_source, predict_start_time):
    if isinstance(model_source, str): 
        model = torch.load(model_source)
    else: 
        model = model_source
    
    if isinstance(data_source, str):
        df = pd.read_csv(open(data_source))
    else:
        df = data_source
    
    features = model['features']
    target_column = model['target_column']
    freq = model['freq']
    time_step = model['time_step']
    prediction_length = model['prediction_length']
    hidden_size = model['hidden_size']
    Quantile = model['Quantile']
    state_dict = model['state_dict']
    scaler_std = model['scaler_std']
    scaler = 10
    
    if 'time' in df.columns.tolist():
        df.index = df.time.astype('datetime64[ns]')
        df >>= drop('time')
       
    df = df[features].astype(float).resample(freq).mean()
    time_index = pd.date_range(df.index[0], periods= len(df) + prediction_length , freq = freq)
    target_column_index = features.index(target_column)
    if df.isnull().values.sum() > 0:
        print("The data source has missing value after aggregated by freq = '{}'".format(freq))
        print("Filling missing value use method = 'pad'")
        df = df.fillna(method = 'pad').dropna()
    
    predict_range = where(time_index >= predict_start_time)[:prediction_length]
    if len(predict_range) < prediction_length:  predict_range = np.arange(len(time_index))[-prediction_length:]
    
    input_data_range = np.arange(predict_range[0] - time_step, predict_range[0])
    if sum(input_data_range < 0) > 0 :
        input_data_range = np.arange(time_step)
        predict_range = np.arange(time_step, time_step + prediction_length)
    
    net = GRU_seq2seq(input_size = len(features),
                      output_size = len(Quantile),
                      hidden_size = hidden_size,
                      time_step = time_step,
                      prediction_length = prediction_length)
    net.load_state_dict(state_dict)
    net.eval()
    
    std_target =  np.sqrt(scaler_std.var_)[target_column_index]
    if std_target == 0: std_target = 1
    mean_target =  scaler_std.mean_[target_column_index]
    
    inpu_data = torch.tensor(scaler_std.transform(df.iloc[input_data_range])).float().unsqueeze(0)/scaler
    pred_result = net(inpu_data).data.numpy()[0]*std_target*scaler + mean_target
    pred_result_dict = {str(q):pred_result[:, i].tolist() for i, q in enumerate(Quantile)}
    
    return {'predict_target': target_column,
            'predict_result': pred_result_dict,
            'time': time_index[predict_range].strftime('%Y-%m-%d %H:%M:%S').tolist()}

def predict_to_gif(data_source, model_source, predict_start_time, filename,
                   ticks_step = 15, size = [15, 7]):
    if isinstance(model_source, str): 
        model = torch.load(model_source)
    else: 
        model = model_source
    
    if isinstance(data_source, str):
        df = pd.read_csv(open(data_source))
    else:
        df = data_source
    
    features = model['features']
    target_column = model['target_column']
    freq = model['freq']
    time_step = model['time_step']
    prediction_length = model['prediction_length']
    Quantile = model['Quantile']
    RMSE_train = model['RMSE_train']
    RMSE_validate = model['RMSE_validate']
    RMSE_test = model['RMSE_test']

    if 'time' in df.columns.tolist():
        df.index = df.time.astype('datetime64[ns]')
        df >>= drop('time')
       
    df = df[features].astype(float).resample(freq).mean()
    time_index = pd.date_range(df.index[0], periods= len(df) + prediction_length , freq = freq)
    target_column_index = features.index(target_column)
    if df.isnull().values.sum() > 0:
        print("The data source has missing value after aggregated by freq = '{}'".format(freq))
        print("Filling missing value use method = 'pad'")
        df = df.fillna(method = 'pad').dropna()

    fname = pkg_resources.resource_filename(__name__, '../Fonts/kaiu.ttf')
    image_list = []
    register_matplotlib_converters()
    fig, ax = plt.subplots()
    for i in predict_start_time:
        pred_result = predict(data_source, model_source, i)
        time_index = pd.date_range(df.index[0], periods = len(df) + len(pred_result['time']), freq = freq)
        time_index_pred = pd.date_range(pred_result['time'][0], periods = len(pred_result['time']), freq = freq)
        diff = (time_index[1] - time_index[0]).total_seconds()
        if diff >= 360*86400:
            time_index_label = time_index.astype(str).str.slice(0, 4)
            title = '{} 未來走勢預測 (預測開始於 {})'.format(target_column, pred_result['time'][0][:4])        
        elif diff >= 20*86400:
            time_index_label = time_index.astype(str).str.slice(0, 7)
            title = '{} 未來走勢預測 (預測開始於 {})'.format(target_column, pred_result['time'][0][:7])
        elif diff >= 86400:
            time_index_label = time_index.astype(str).str.slice(0, 10)
            title = '{} 未來走勢預測 (預測開始於 {})'.format(target_column, pred_result['time'][0][:10])
        elif diff >= 3600:
            time_index_label = time_index.astype(str).str.slice(0, 13)
            title = '{} 未來走勢預測 (預測開始於 {})'.format(target_column, pred_result['time'][0][:13])
        elif diff >= 60:
            time_index_label = time_index.astype(str).str.slice(0, 16)
            title = '{} 未來走勢預測 (預測開始於 {})'.format(target_column, pred_result['time'][0][:16])    
        else:
            time_index_label = time_index.astype(str)
            title = '{} 未來走勢預測 (預測開始於 {})'.format(target_column, pred_result['time'][0])

        font = FontProperties(fname = fname, size = 15)
        fig.set_size_inches(*size)
        p1 = ax.plot(df[target_column], 'b')[0]
        p2 = ax.plot(time_index_pred, pred_result['predict_result'][str(Quantile[0])], 'r')[0]
        p3 = ax.fill_between(time_index_pred,  pred_result['predict_result'][str(Quantile[1])],  pred_result['predict_result'][str(Quantile[2])], color = 'c')
        p4 = ax.plot([], [], ' ')[0]
        ax.legend([p1, p2, p3, p4, p4, p4], 
                ('實際值', '預測值', '{:.0%} 預測區間'.format(Quantile[2]-Quantile[1]), 
                '訓練集 RMSE = {:.4f}'.format(RMSE_train), 
                '驗證集 RMSE = {:.4f}'.format(RMSE_validate),
                '測試集 RMSE = {:.4f}'.format(RMSE_test)      )
                , loc='best', prop=font)
        ax.set_xticks(time_index[::ticks_step])
        ax.set_xticklabels(time_index_label[::ticks_step])
        ax.set_ylabel(target_column, fontproperties=font, fontsize = 20)
        ax.set_xlabel('時間', fontproperties=font, fontsize = 20) 
        ax.set_title(title, fontproperties=font, fontsize = 30, y = 1.03)
        buf = io.BytesIO()            
        fig.savefig(buf)
        plt.cla()
        buf.seek(0)
        image_list.append(imageio.imread(buf))
    imageio.mimsave(filename, image_list, duration=1.5)
