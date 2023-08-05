from setuptools import setup, find_packages

exec (open('myDL/version.py').read())

setup(
    name='myDL',
    version=__version__,
    author='jimmybow',
    author_email='jimmybow@hotmail.com.tw',
    packages=find_packages(),
    url = 'https://github.com/jimmybow/myDL',
    include_package_data = True,
    license='BSD',
    description='my deep learning',
    install_requires=['mydf', 'imageio'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]   
)
