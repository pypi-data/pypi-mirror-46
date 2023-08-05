#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse
#       文件名: setup.py
#       作者  : Qazse
#       时间  : 2019/4/13
#       主页  : http://qiiing.com
#       功能  :
# ---------------------------------------------------

from setuptools import setup, find_packages

setup(
    name='qazse',
    version="0.8.0",
    keywords=("pip", "qazse", "QazseWong"),
    packages=find_packages(),
    author='QazseWong',
    author_email='w@qiiing.com',
    url='http://w.qiiing.com',
    license="MIT Licence",
    description='自己用的工具包',
    long_description="自己python项目常用得工具包",
    include_package_data=True,
    platforms="any",
    install_requires=["redis","requests","aiohttp","asyncio","bs4",
                      "selenium","pymongo","qiniu",'pymysql',
                      'sqlacodegen','w3lib']
)
