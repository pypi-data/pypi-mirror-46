#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setup.py.py
@Version :   1.0.0
@Author  :   xiaxianba
@License :   (C) Copyright 2006-2019
@Contact :   xiaxianba@qq.com
@Software:   PyCharm
@Time    :   2019/5/6 14:08
@Desc    :
"""

from setuptools import setup, find_packages
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


long_desc = """
Data Drawer
===============

Target Users
--------------
* financial market analyst of China
* learners of financial data analysis with pandas/NumPy
* people who are interested in China financial data
Installation
--------------
    pip install datadrawer

Upgrade
---------------
    pip install datadrawer --upgrade
"""


def read_install_requires():
    reqs = [
        'pandas>=0.23.4',
        'requests>=2.0.0',
        'lxml>=3.8.0',
        'simplejson>=3.16.0',
        'numpy>=1.11.3',
        'matplotlib>=1.5.1'
    ]
    return reqs


setup(
    name='datadrawer',
    version=read('datadrawer/VERSION.txt'),
    description='A Fast Tool for Data Processing and Powerful Toolset',
    #     long_description=read("READM.rst"),
    long_description=long_desc,
    author='Xia Xianba',
    author_email='xiaxianba@qq.com',
    license='BSD',
    url='https://github.com/xianba/datadrawer',
    install_requires=read_install_requires(),
    keywords='Data Drawer',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'License :: OSI Approved :: BSD License'],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)