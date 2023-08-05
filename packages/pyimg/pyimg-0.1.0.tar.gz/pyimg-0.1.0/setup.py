# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pyimg

PKG_NAME = "pyimg"
VERSION = pyimg.__version__
DESCRIPTION = "Image analysis utilities in Python"
HOMEPAGE = "https://github.com/PingjunChen/pyimg"
LICENSE = "MIT"
AUTHOR_NAME = "Pingjun Chen"
AUTHOR_EMAIL = "chenpingjun@gmx.com"

REQS = ""
with open('requirements.txt') as f:
    REQS = [pkg.replace("==", ">=") for pkg in f.read().splitlines()]

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering',
]

args = dict(
    name=PKG_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=HOMEPAGE,
    license=LICENSE,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=REQS,
    classifiers= CLASSIFIERS,
)

setup(**args)
