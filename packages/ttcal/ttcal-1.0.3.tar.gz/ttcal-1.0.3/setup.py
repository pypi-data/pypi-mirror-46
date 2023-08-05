#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ttcal - calendar operations
===========================
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.6
Topic :: Software Development :: Libraries
"""

import sys, os
import setuptools
from distutils.core import setup, Command
from setuptools.command.test import test as TestCommand

version = '1.0.3'

DIRNAME = os.path.dirname(__file__)
description = open(os.path.join(DIRNAME, 'README.rst'), 'rb').read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='ttcal',
    version=version,
    url='https://github.com/datakortet/ttcal',
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    requires=[],
    install_requires=[
        'six',
        'future',
    ],
    # description=__doc__.strip(),
    long_description=description,
    classifiers=[line for line in classifiers.split('\n') if line],
    cmdclass={'test': PyTest},
    packages=['ttcal'],
    zip_safe=False,
)
