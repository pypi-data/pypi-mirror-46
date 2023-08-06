#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requisites = ['requests-html>=0.10.0']

setup(
    name='uds',
    version='0.1.0',
    description='Search UrbanDictionary',
    long_description=open('README.md').read(),
    author='Viet Hung Nguyen',
    author_email='hvn@familug.org',
    url='https://github.com/hvnsweeting/uds',
    license='MIT',
    classifiers=[
        'Environment :: Console',
    ],
    scripts=['uds'],
)
