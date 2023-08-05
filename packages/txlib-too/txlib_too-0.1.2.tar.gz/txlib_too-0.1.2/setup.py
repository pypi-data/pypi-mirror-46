#!/usr/bin/env python
import versioneer

from setuptools import setup, find_packages


setup(
    version='0.1.2',

    name="txlib_too",
    author="eb-pypi",
    author_email="eb-pypi@eventbrite.com",

    description="A python library for Transifex",
    url="http://www.eventbrite.com",

    packages=find_packages(),
    install_requires=[
        "requests",
        "six"
    ],

    long_description=open('README.rst').read(),

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=(
        'translation',
        'localization',
        'internationalization',
    ),
    license='LGPL3',
)
