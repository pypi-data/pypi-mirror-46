#!/usr/bin/env python

""""
The MIT License (MIT)

Copyright (c) 2016 Esbjorn Blomquist, Jesper Ahlberg, Mikael Magnusson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from setuptools import setup
from pytiip.tiip import __version__ as version

fixed_version=version[5:]
if len(fixed_version.split(".")) <3:
    fixed_version += ".2"

setup(
    name='pytiip',
    version=fixed_version,
    description='TIIP-protocol implementation for Python',
    keywords='Industrial Internet Things Protocol',
    author='Esbjorn Blomquist, Jesper Ahlberg, Mikael Magnusson',
    license='MIT License',
    url="https://github.com/MickMack1983/pytiip.git",
    author_email="mikael.m.magnusson@gmail.com",
    packages=[
        'pytiip'
    ],
    install_requires=[
        'python-dateutil'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'

    ]
)
