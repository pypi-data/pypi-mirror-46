#!/usr/bin/env python

import os.path

from setuptools import setup

# get the version to include in setup()
dir_ = os.path.abspath(os.path.dirname(__file__))
with open(f'{dir_}/asyncio_multisubscriber_queue/__init__.py') as fh:
    for line in fh:
        if '__version__' in line:
            exec(line)


setup(
    name='asyncio-multisubscriber-queue',
    version=__version__,
    license='MIT',
    author='Kyle Smith',
    author_email='smithk86@gmail.com',
    url='https://github.com/smithk86/asyncio-multisubscriber-queue',
    packages=['asyncio_multisubscriber_queue'],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: AsyncIO',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
