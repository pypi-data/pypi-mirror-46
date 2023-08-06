#!/usr/bin/env python

import ast
import os
import re
import sys

from pyArchery import __version__ as version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r') as f:
    readme = f.read()

# Publish helper
if sys.argv[-1] == 'build':
    os.system('python setup.py sdist bdist_wheel')
    sys.exit(0)

if sys.argv[-1] == 'install':
    os.system('python setup.py sdist --formats=zip')
    sys.exit(0)

setup(
    name='pyArchery',
    packages=['pyArchery'],
    version=version,
    description='Python library enumerating the Archery tool RESTFul API endpoints.',
    long_description=readme,
    author='Anand Tiwari',
    author_email='anandtiwarics@gmail.com',
    url='https://github.com/archerysec/',
    license='MIT License',
    zip_safe=True,
    install_requires=['requests'],
    keywords=['pyArchery', 'api', 'security', 'software', 'ArcherySec'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
    ]
)

