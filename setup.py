#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lijin
# Mail: lijin@dingtalk.com
# Created Time:  2019-08-16
#############################################


from setuptools import setup, find_packages

setup(
    name = "AliFCWeb",
    version = "0.1.0",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),							
    description = "阿里云函数计算web框架",
    long_description = "简易的阿里云函数计算web框架",
    license = "MIT Licence",

    url = "https://github.com/l616769490/ali-fc-web",
    author = "lijin",
    author_email = "lijin@dingtalk.com",

    packages = find_packages(),	
    include_package_data = True,
    platforms = "any",
    install_requires = []
)