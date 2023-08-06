#!/usr/bin/env python
# -*- coding: utf8 -*-
# Author: Tony <stayblank@gmail.com>
# Create: 2019/5/26 22:09
from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
    name="time-kong",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PurpleSun/time_kong",
    version="0.0.1",
    keywords=("time", "transform", "convert"),
    description="A useful time transform util, transforms between string, timestamp and datetime format",
    license="MIT License",
    install_requires=[],
    author="fanwei.zeng",
    author_email="stayblank@gmail.com",
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    platforms="any"
)
