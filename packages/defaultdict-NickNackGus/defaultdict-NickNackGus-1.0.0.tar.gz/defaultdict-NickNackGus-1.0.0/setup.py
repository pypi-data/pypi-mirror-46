#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="defaultdict-NickNackGus",
    version="1.0.0",
    author="NickNackGus",
    author_email="NickNackGus@gmail.com",
    description="defaultdict with deepcopy support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NickNackGus/pydefaultdict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
