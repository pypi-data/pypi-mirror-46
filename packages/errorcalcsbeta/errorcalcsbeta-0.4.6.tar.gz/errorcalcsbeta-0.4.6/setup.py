# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='errorcalcsbeta',
    version='0.4.6',
    description='GUI for error calulations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonfrcom/errorcalcs-beta",
    author='lefrcom',
    author_email='lefrcom@gmx.de',
    packages=['errorcalcsbeta'],
    install_requires=[
        'uncertainties',
        'PyQt5',
        'sympy',
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
