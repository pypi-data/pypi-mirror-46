# Script: setup.py
# Author: Kurt Collins (@timesync)
# 
# The setuptools script for the slice audio tool.


################################################################################
# Imports
################################################################################

from setuptools import find_packages, setup


################################################################################
# Configuration
################################################################################

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='audio-slice',
    version='0.0.6',
    author="Kurt Collins",
    author_email="kurt@kurt.sx",
    description="A command line utility to slice MP3 files into pieces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shebanginc/audio-slice",
    packages=find_packages(),
    py_modules=['slice'],
    install_requires=[
        'Click',
        'pydub'
    ],
    entry_points='''
        [console_scripts]
        slice=slice:cli
    ''',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)