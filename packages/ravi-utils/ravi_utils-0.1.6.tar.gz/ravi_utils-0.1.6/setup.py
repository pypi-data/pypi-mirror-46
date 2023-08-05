# -*- coding: utf-8 -*-
"""Setup for package """

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ravi_utils',
    version='0.1.6',
    author='Raul Viigipuu',
    author_email='raul@viigipuu.ee',
    description='Common functions package for simple scripts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/raulviigipuu/ravi_utils',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
