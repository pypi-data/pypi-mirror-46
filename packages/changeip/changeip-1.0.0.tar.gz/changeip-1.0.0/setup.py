#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Huzhiyong
# Mail: huzhiyong777@gmail.com
# Created Time:  2019-5-16 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "changeip",      #这里是pip项目发布的名称
    version = "1.0.0",  #版本号，数值大的会优先被pip
    keywords = ("pip", "changeip","privoxy"),
    description = "changeip",
    long_description = "changeip auto",
    license = "MIT Licence",

    url = "",     #项目相关文件地址，一般是github
    author = "Huzhiyong",
    author_email = "huzhiyong777@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    #install_requires = ["numpy"]          #这个项目需要的第三方库
)
