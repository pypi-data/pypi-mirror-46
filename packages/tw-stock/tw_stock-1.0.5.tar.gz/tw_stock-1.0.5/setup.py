# coding: utf-8
import codecs
import os
import sys
from setuptools import setup, find_packages

VERSION = "1.0.5"
LICENSE = "MIT"

with open('README.md', 'rb') as fp:
    readme = fp.read()

setup(
    name='tw_stock',
    version=VERSION,
    description=(
        'Get Taiwan\'s stock info in real-time'
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Jasper',
    author_email='jiunway@gmail.com',
    maintainer='Jasper',
    maintainer_email='jiunway@gmail.com',
    license=LICENSE,
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/jiunway/tw_stock',
    download_url="",
    keywords=['stock', 'tw', 'taiwan stock'],
    classifiers=[]
)
