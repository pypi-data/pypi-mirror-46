#! -*- coding:UTF-8 -*- 
import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup


 
def read(fname):

    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
 
NAME = "pysogo"

PACKAGES = ["pysogo",]

DESCRIPTION = "A simple Sogo browser with python."

 
LONG_DESCRIPTION = read("README.rst")

 
KEYWORDS = "pysogo"

AUTHOR = "chinming"

 
AUTHOR_EMAIL = "chinming95@foxmail.com"

URL = "https://github.com/cchinm/python-spider/tree/master/entertainment/pybrowser"

VERSION = "0.0.2"

 
LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)