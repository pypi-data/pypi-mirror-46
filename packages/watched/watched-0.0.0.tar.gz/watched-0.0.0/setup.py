#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from distutils.command.upload import upload as UploadOrig

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = 'watched'
DESCRIPTION = "It's like watch, but with history."
URL = 'https://github.com/chhabrakadabra/watched'
EMAIL = 'chhabra.abhin@gmail.com'
AUTHOR = 'Abhin Chhabra'
REQUIRES_PYTHON = '>3.7'
LICENSE = 'MIT License'
COPYRIGHT = 'Copyright 2019 Abhin Chhabra'

REQUIRED = [

]

SETUP_REQUIRED = [
    'setuptools_scm'
]

EXTRAS = {
    'tests': [
        'pytest',
    ],
    'linter': [
        'flake8',
        'flake8-broken-line',
        'flake8-builtins',
        'flake8-bugbear',
        'flake8-comprehensions',
        'flake8-eradicate',
        'flake8-pep3101',
        'flake8-print',
        'flake8-quotes',
    ]
}

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    use_scm_version=True,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=REQUIRED,
    setup_requires=SETUP_REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    copyright=COPYRIGHT,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
