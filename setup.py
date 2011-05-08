#!/usr/bin/env python

from distutils.core import setup

SUMMARY="Assign arbitrary order to a directory's contents"
DESCRIPTION = "\n" + file("description").read()
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: Public Domain",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Topic :: System :: Filesystems",
    "Topic :: Utilities",
    ]

setup(
    name="Itemize",
    version="0.2",
    description=SUMMARY,
    long_description=DESCRIPTION,
    author="Frank DeMarco",
    author_email="frank.s.demarco@gmail.com",
    url="http://squd.org/tools/itemize",
    packages=["itemize"],
    scripts=["src/itemize"],
    package_dir={"itemize" : "src"},
    classifiers=CLASSIFIERS
    )
