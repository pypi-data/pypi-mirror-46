#!/usr/bin/env python
import os.path
from sys import stderr
from setuptools import setup

from grepme import VERSION, HOMEPAGE
DESCRIPTION = 'grep for GroupMe'
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='grepme',
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joshua Nelson',
    author_email='jyn514@gmail.com',
    license='BSD',
    keywords='grep search chat web groupme',
    url=HOMEPAGE,
    py_modules=["grepme", "login"],
    entry_points = {
        'console_scripts': ['grepme=grepme:main']
    },
    install_requires=['requests', 'keyring==10'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat"
    ]
)
