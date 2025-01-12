#!/usr/bin/env python

from __future__ import annotations

from setuptools import setup, find_packages

setup(
    name="distronode_test_pip_chdir",
    version="0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'distronode_test_pip_chdir = distronode_test_pip_chdir:main'
        ]
    }
)
