#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

__name__ = 'monkey.ioc'
__version__ = "0.0.1.dev1"
__author__ = 'Xavier ROY'
__author_email__ = 'xavier@regbuddy.eu'

_packages = find_packages()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://bitbucket.org/monkeytechnologies/monkey-ioc/',
    description='Simple IOC framework agile as a monkey.',
    long_description=open('README.md').read(),
    license="Apache License, Version 2.0",

    packages=_packages,
    include_package_data=True,

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Intended Audience :: Developers'
    ]
)
