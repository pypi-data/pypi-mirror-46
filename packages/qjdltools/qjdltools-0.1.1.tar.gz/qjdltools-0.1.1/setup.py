#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="qjdltools",
    version="0.1.1",
    author="Ji Qi",
    author_email="51978200@qq.com",
    description="Some simple tools for deep learning.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/ErenTuring/dl_tools",
    packages=['qjdltools'],
    install_requires=[
        'h5py', 'matplotlib', 'opencv-python', 'tqdm',
        'scipy', 'scikit-image',
        ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
