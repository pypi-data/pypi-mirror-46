#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import mctest

# with open("README.md", "r", encoding='utf-8') as fh:
#     long_description = fh.read()

setup(
    name="mctest",
    version='0.0.1',
    author="HGzhao",
    author_email="nqzjf123@126.com",
    description="for mc_api test",
    long_description=' ',
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/HGzhao/MagCore_GameClient",
    packages=find_packages(),
    install_requires=[ ],
    classifiers=[
        "Topic :: Games/Entertainment ",
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Games/Entertainment :: Board Games',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)