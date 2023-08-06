#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import versify

install_requires = ['requests==2.21.0', 'configparser==3.7.4']

setup(

    name='versify',

    version=versify.__version__,

    packages=find_packages(),

    author="Willy K.",

    author_email="willy.konguem@gmail.com",

    description="Client for DBT API Platform",

    long_description=open('README.rst').read(),

    install_requires=install_requires,

    include_package_data=True,

    url='https://github.com/willinprogress/python-versify',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
