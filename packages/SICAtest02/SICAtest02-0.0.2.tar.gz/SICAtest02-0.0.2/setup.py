#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages

setup(
    name = "SICAtest02",
    version = "0.0.2",
    keywords = ("pip_test", "SICA_test","featureextraction_test","test!!"),
    description = "An feature extraction algorithm,   local repo testing",
    long_description = "An feature extraction algorithm, improve the FastICA test",
    license = "MIT Licence test",

    url = "https://github.com/yifanff/sica_test_0513",
    author = "Yifan",
    author_email = "yifanff@126.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]
)
