#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://jet-python.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='jet-python',
    version='0.2',
    description='Python Jet.com API Client',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Fulfil.IO Inc.',
    author_email='tech-support@fulfil.io',
    url='https://github.com/fulfilio/jet-python',
    packages=[
        'jet',
    ],
    package_dir={'jet': 'jet'},
    include_package_data=True,
    install_requires=[
        'python-dateutil',
        'requests',
    ],
    license='MIT',
    zip_safe=False,
    keywords='jet jet.com python',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
