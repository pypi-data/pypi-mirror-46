#!/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r') as rm:
    long_description = rm.read()

setup(
    name = 'radius',
    version = '0.0.3',
    description = 'RADIUS authentication module',
    long_description=long_description,
    author = 'Stuart Bishop',
    author_email = 'zen@shangri-la.dropbear.id.au',
    maintainer = 'Osirium',
    maintainer_email = 'thomas.grainger@osirium.net',
    url = 'https://github.com/Osirium/py-radius/',
    py_modules = ["radius"],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ]
)
