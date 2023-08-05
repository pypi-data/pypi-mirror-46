#!/usr/bin/env python
# -*- coding: utf-8 -*

from __future__ import absolute_import

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('README.rst', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.rst', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

setup(
    name='imdbpie',
    version='5.6.4',
    packages=find_packages('src', exclude=('tests',)),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    description=(
        'Python IMDB client using the IMDB json web service made '
        'available for their iOS app.'
    ),
    author='Richard O\'Dwyer',
    author_email='richard@richard.do',
    url='https://code.richard.do/richardARPANET/imdb-pie/',
    license='Apache 2.0',
    long_description=readme + '\n\n' + history,
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
