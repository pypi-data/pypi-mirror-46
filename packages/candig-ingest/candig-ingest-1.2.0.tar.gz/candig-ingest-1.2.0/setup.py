#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "docopt",
    "candig-server",
    "pandas",
    ]

setup_requirements = [
    ]

test_requirements = [
    ]

setup(
    name='candig-ingest',
    version='1.2.0',
    description='Routines for ingesting metadata to a CanDIG repository',
    long_description='\n\n'.join((readme, history)),
    url='https://github.com/CanDIG/candig-ingest.git',
    author='CanDIG team',
    author_email='info@distributedgenomics.ca',
    packages=find_packages(include=['candig', 'candig.ingest']),
    namespace_packages=['candig'],
    entry_points={
        'console_scripts': [
            'ingest=candig.ingest.ingest:main',
            'load_tier=candig.ingest.load_tiers:main',
            ]
        },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    license="GNU General Public License v3",
    keywords='candig-ingest',
   )
