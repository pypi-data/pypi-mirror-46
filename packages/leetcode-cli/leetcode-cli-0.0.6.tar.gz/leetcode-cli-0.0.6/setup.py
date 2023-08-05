#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leetcode-cli",
    version="0.0.6",
    author="Pengcheng Chen",
    author_email="pengcheng.chen@gmail.com",
    description="LeetCode CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenpengcheng/cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="leetcode",
    include_package_data=True,
    install_requires=[
        "ascii_graph",
        "bs4",
        "PyExecJS",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "leetcode-cli=leetcodecli.cli:main",
        ],
    },
)
