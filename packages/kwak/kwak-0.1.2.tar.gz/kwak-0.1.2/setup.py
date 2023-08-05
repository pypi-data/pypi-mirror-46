from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'kwak',
    packages=find_packages(),
    version='0.1.2',
    url='https://github.com/alexxromero/kwak_wavelets',
    author='Ben G. Lillard and Alexis Romero',
    author_email='alexir2@uci.edu',
    license='MIT',
    description='Statistical tool for wavelet analysis',
    )
