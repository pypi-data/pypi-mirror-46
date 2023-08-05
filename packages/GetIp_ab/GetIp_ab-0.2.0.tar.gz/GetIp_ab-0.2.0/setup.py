# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="GetIp_ab",
    version="0.2.0",
    author="Arbert",
    author_email="anbang_li@163.com",
    description="a simple program to get proxies",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/aaadrain",
    packages=['GetIp'],
    install_requires=[
        "beautifulsoup4",
        'requests',
        'fake_useragent',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
