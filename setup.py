"""Setup configuration for the package."""
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import versioneer

# pylint: disable=invalid-name
long_desc = """Deliberd is a comprehensive program that serves as a unified gateway to a multitude of large-scale models. It supports a wide array of domestic major models such as QianWen, Wenxin, XingHuo, and BaiChuan, thereby enabling seamless interaction and access to these leading AI models within China's landscape."""

setup(
    name="delibird",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url="https://github.com/EeroEternal/delibird",
    author="lipi",
    author_email="lipicoder@qq.com",
    description="LLM unified server",
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
