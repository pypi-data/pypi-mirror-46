#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='pysogo',
    version='0.0.1',
    description=(
        'A simple browser with python'
    ),
    long_description=open('README.rst').read(),
    author='chinming',
    author_email='chinming95@foxmail.com',
    maintainer='chinming',
    maintainer_email='chinming95@foxmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/cchinm/python-spider/tree/master/entertainment/pybrowser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)