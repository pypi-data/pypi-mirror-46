#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:yangtao
@file: setup.py
@time: 2019/05/22
"""
from setuptools import setup, find_packages

setup(
    name="operate_excel",
    version="0.1.1",
    author="Tao Yang",
    description="Excel operation method",
    author_email="1724805202@qq.com",
    packages=find_packages(),
    platforms=["all"],
    license="MIT",
    url="https://github.com/ChristianYangTao/opetate_excel.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
