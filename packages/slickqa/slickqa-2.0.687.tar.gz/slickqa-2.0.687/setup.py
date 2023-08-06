#!/usr/bin/env python

from setuptools import setup, find_packages

__author__ = 'Jason Corbett'


def get_requirements(filename):
    with open(filename) as f:
        return f.readlines()

setup(
    name="slickqa",
    description="A client library for the Slick QA result database",
    version="2.0.687",
    license="License :: OSI Approved :: Apache Software License",
    long_description=open('README.rst').read(),
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rst', '*.html']},
    include_package_data=True,
    install_requires=get_requirements('requirements.txt'),
    author="Slick Developers",
    url="http://github.com/slickqa/python-client"
)
