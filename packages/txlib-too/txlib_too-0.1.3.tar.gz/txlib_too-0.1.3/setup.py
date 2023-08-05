#!/usr/bin/env python
import versioneer

from setuptools import setup, find_packages


setup(
    version='0.1.3',
    # cmdclass=versioneer.get_cmdclass(),

    name="txlib_too",
    author="Indifex Ltd.",
    author_email="info@indifex.com",

    description="A python library for Transifex",
    url="http://www.indifex.com",

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
    keywords=[
        'translation',
        'localization',
        'internationalization',
    ],
    license='LGPL3',
)
