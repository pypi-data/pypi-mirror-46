#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import os
import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename, 'r') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version(os.path.join('gargoyle', '__init__.py'))

with open('README.rst', 'r') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', 'r') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='gargoyle-yplan',
    version=version,
    author='DISQUS',
    author_email='opensource@disqus.com',
    maintainer='Adam Johnson',
    maintainer_email='me@adamj.eu',
    url='https://github.com/adamchainz/gargoyle',
    description=(
        'Gargoyle is a platform built on top of Django which allows you to switch functionality of your application '
        'on and off based on conditions.'
    ),
    long_description=readme + '\n\n' + history,
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    install_requires=[
        'Django>=1.11',
        'django-modeldict-yplan>=2.0.0',
        'nexus-yplan>=2.1.0',
        'django-jsonfield>=1.2.0',
    ],
    python_requires='>=3.4',
    license='Apache License 2.0',
    include_package_data=True,
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
