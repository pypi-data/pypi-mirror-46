#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: handa
# Mail: 794363716@qq.com.com
# Created Time:  2018-09-19 18:18:18
#############################################


from setuptools import setup, find_packages

setup(
    name = "fasterGit",
    version="0.1.1",
    keywords = ("pip", "git", "gitHost", "host"),
    description = "Modify the host file to improve the speed of pulling git code",
    long_description = "Modify the host file to improve the speed of pulling git code",
    license = "MIT Licence",

    url="https://github.com/WendStation/fasterGit",
    author="handa",
    author_email="794363716@qq.com",
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # include any *.msg files found in the 'test' package, too:
        'test': ['*.msg'],
    },
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["PyYAML"],
    entry_points={'console_scripts': [
        "fasterGit = fasterGit.fasterGit:main",
    ]}
)