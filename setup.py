# -*- coding: utf-8 -*-
try:
    from setuptools import find_packages, setup
except ImportError:
    import distribute_setup

    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

import os
import sys
from distutils import log

long_desc = """delibird is a python tool library based on Python pyarrow which supports multithread and asynchronous calls. It can help users transform data between database and Parquet files."""

requires = ["pyarrow", "psecopy", "click"]

setup(
    name="delibird",
    version="0.0.5",
    url="https://github.com/lipicoder/delibird",
    license="MIT License",
    author="lipi,zhujw",
    author_email="lipicoder@qq.com, kratoswittgenstein@gmail.com",
    description="Exchange data between database and parquet files",
    long_description=long_desc,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
