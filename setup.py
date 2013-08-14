#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois

import os
import re

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    path_components = package_components + ['__init__.py']
    with open(os.path.join(root_dir, *path_components)) as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


def parse_requirements(requirements_file):
    with open(requirements_file, 'r') as f:
        return [line for line in f if line.strip() and not line.startswith('#')]


PACKAGE = 'batchform'
REQUIREMENTS_PATH = 'requirements.txt'


setup(
    name="django-batchform",
    version=get_version(PACKAGE),
    author="Raphaël Barrois",
    author_email="raphael.barrois+batchform@polytechnique.org",
    description="Fill a batch of django forms from an uploaded file.",
    license="BSD",
    keywords=['django', 'form', 'batch', 'upload'],
    url="http://github.com/rbarrois/django-batchform",
    download_url="http://pypi.python.org/pypi/django-batchform/",
    packages=[
        'batchform',
        'batchform.parsers',
    ],
    package_data={
        'batchform': [
            'static/batchform/css/*.css',
            'static/batchform/js/*.js',
            'templates/batchform/*.html',
        ],
    },
    setup_requires=[
        'setuptools>=0.8',
    ],
    install_requires=parse_requirements(REQUIREMENTS_PATH),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

