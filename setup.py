#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='apistar-aws-xray',
    version='0.1.0',
    author='Ben Harling',
    author_email='bharling@crowdcomms.co.uk',
    maintainer='Ben Harling',
    maintainer_email='bharling@crowdcomms.co.uk',
    license='MIT',
    url='https://github.com/bharling/apistar-aws-xray',
    description='AWS Xray tracing middleware for API Star',
    long_description=read('README.rst'),
    py_modules=['apistar_aws_xray'],
    python_requires='>=3.5',
    install_requires=[
        'pytest>=3.5.0', 'apistar>=0.5.41', 'aws-xray-sdk>=1.1.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ]
)
