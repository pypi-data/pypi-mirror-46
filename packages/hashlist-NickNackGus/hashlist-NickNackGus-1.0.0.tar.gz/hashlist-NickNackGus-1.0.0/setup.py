#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hashlist-NickNackGus",
    version="1.0.0",
    author="NickNackGus",
    author_email="NickNackGus@gmail.com",
    description="Compare differences in list order with minimal insertions/deletions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NickNackGus/pyhashlist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "defaultdict-NickNackGus"
    ]
)
