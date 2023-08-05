#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages
print(find_packages())
setup(
    name = "KuaiShouGetCnString",
    version = "0.1.2",
    keywords = ("pip", "KuaiShouGetCnString"),
    description = "A font processing function ",
    long_description = "A font processing function ",
    license = "MIT Licence",

    url = "https://github.com/jinmingzhou/KuaiShouGetCnString",
    author = "robin",
    author_email = "1983273232@qq.com",
    packages =['.'],
    include_package_data = True,
    platforms = "any",
    install_requires = []
)