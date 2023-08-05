"""
torch-utils
Common Utils for PyTorch
Author: SF-Zhou
Date: 2019-04-11
"""

from setuptools import find_packages, setup

name = 'torch-utils'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.1.1',
    description='Common Utils for PyTorch',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='PyTorch Utils',
    packages=find_packages(exclude=['tests']),
    install_requires=['torch']
)
