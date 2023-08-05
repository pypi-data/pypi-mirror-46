#!/usr/bin/env python  #add this to make sure ***.py run in terminal
# -*- coding: utf-8 -*- #add this to make sure ***.py read by utf-8

'【工资模块】安装描述'
__author__ = 'egret'

from distutils.core import setup

import ssl
import urllib3
ssl._create_default_https_context = ssl._create_unverified_context
# print urllib2.urlopen("https://www.111cn.net/").read()

setup(
    name='salaryModel',
    version='1.0',
    description='工资计算模块',
    author='egret',
    author_email='906932256@qq.com',
    py_modules=['salaryModel.xdl_001_Salary']
)