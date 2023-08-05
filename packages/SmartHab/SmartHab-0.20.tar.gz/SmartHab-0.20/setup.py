#!/usr/bin/env python3

from setuptools import (setup, find_packages)

setup(
    name="SmartHab",
    version="0.20",
    packages=find_packages(),
    author="Baptiste Candellier",
    author_email="outadoc@gmail.com",
    description="This package allows controlling devices in a SmartHab-powered home.",
    install_requires=[
        'requests'
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/outadoc/python-smarthab/",
    test_suite="test_smarthab",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Home Automation"
    ]
)
