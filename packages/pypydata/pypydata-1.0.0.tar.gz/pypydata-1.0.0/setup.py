#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypydata',
    version='1.0.0',
    description='PypyData Location List',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ryuih/pypydata',
    author='iryu',
    author_email='inhwanryu@gmail.com',
    license='MIT',
    install_requires=['beautifulsoup4', 'lxml'],
    keywords='pypydata',
    packages=find_packages(exclude=('tests')),
    entry_points={
        "console_scripts": [
            "pypydata=pypydata.__init__:main",
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
