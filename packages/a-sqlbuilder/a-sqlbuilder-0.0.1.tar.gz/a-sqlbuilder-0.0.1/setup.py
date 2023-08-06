#!/usr/bin/env python

import re
import setuptools

version = ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="a-sqlbuilder",
    version='0.0.1',
    author="aiden.li",
    author_email="1334435738@qq.com",
    description="MySQL chained operation of Python development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lizhenggan/ABuilder",
    install_requires=[
        'pymysql>=0.9.3'
    ],
    packages=setuptools.find_packages(exclude=("test")),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ),
    # exclude_package_data={'': ["example-pkg/test.py", "example-pkg/config.txt"]},
)
