#!/usr/bin/env python

# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Python SDK.
#  For full information on usage and licensing, see https://chirp.io
#
#  Copyright (c) 2011-2019, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

import os
import re
from setuptools import setup, Extension
import sys

vstr = open('chirpsdk/__init__.py', 'r').read()
regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
version = re.search(regex, vstr, re.M)

setup(
    name='chirpsdk',
    version=version.group(1),
    description='Chirp Python SDK',
    long_description='The Chirp Python SDK enables the user to send '
                     'and receive data using the device\'s microphone and speaker.',
    license='License :: Other/Proprietary License',
    author='Asio Ltd.',
    author_email='developers@chirp.io',
    url='https://developers.chirp.io',
    packages=['chirpsdk', 'tests', 'bin'],
    ext_modules=[Extension('_connect', ['chirpsdk/_connect.c'])],
    install_requires=[
        'sounddevice>=0.3.12', 'pysoundfile>=0.9.0', 'configparser>=3.5.0',
        'requests>=2.18.1', 'requests-futures>=0.9.7'
    ],
    include_package_data=True,
    tests_require=['mock==2.0.0'],
    keywords=['sound', 'networking', 'chirp'],
    scripts=[
        'bin/chirp-audio-read', 'bin/chirp-audio-write',
        'bin/chirp-receive', 'bin/chirp-send'
    ],
    test_suite='tests',
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Communications',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
