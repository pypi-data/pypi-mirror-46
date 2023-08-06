#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from distutils.core import setup
from setuptools import setup, find_packages
import MF_StatusCode

setup(
    name="MF_StatusCode",
    version=MF_StatusCode.__version__,
    description="蝰蛇软件工作室-状态管理包",
    author="林睿霖",
    author_email="limitlin@outlook.com",
    maintainer='林睿霖',
    maintainer_email='limitlin@outlook.com',
    url="https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MF_statusCode_python",
    packages=find_packages(),
)
