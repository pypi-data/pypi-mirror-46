#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name="MF_Version",
    version="1.0.1",
    description="蝰蛇软件工作室-版本号操作包",
    author="林睿霖",
    author_email="limitlin@outlook.com",
    maintainer='林睿霖',
    maintainer_email='limitlin@outlook.com',
    url="https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MF_version_python",
    packages=["MF_Version"],
    install_requires=[
        "MF_File>=1.0.4"],
    package_data={'MF_File': ['*.json']}
)