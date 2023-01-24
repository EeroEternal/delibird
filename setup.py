"""Setup configuration for the package."""
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import versioneer

# pylint: disable=invalid-name
long_desc = """delibird is a python tool library based on Python pyarrow \
which supports multithread and asynchronous calls. \
It can help users transform data 
between database and Parquet files."""

setup(
    name="delibird",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url="https://github.com/lipicoder/delibird",
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
)
