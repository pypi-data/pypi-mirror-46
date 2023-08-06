#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/5/23 10:36
# @File : __init__.py
# @Author : Wangji
# @Software: PyCharm

from setuptools import setup, find_packages

setup(
    name='Flask_Mysql_Html',
    version='1.0.2',
    keywords='flask look mysql html',
    description='a look mysql html',
    license='MIT License',
    url='https://github.com/wj844908240/Flask_Mysql_Html.git',
    author='wangji',
    author_email='844908240@qq.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=["flask", "pymysql"]
)
