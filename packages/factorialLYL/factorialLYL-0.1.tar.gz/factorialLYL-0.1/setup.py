# !usr/bin/env python3
# -*- coding: utf-8 -*-
"""Factorial project"""
from setuptools import find_packages, setup

setup(name = 'factorialLYL',    # 注意这里的name不要使用factorial相关的名字，因为会重复， 需要另外取一个不会与其他人冲吃饭的名字
	version = '0.1',
	description = "Factorial module",
	long_description = 'A test module for our book.',
	platforms = ['Linux'],
	author="LYL",
	author_email="dalongxiabj@163.com",
	url="http://www.shiyanlou.com.courses/596",
	license = "MIT",
	packages=find_packages()
	)