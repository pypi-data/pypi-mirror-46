#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import setuptools
import setuptools.command.test
from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('notification_service')


# -*- Command: setup.py test -*-

class pytest(setuptools.command.test.test):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest as _pytest
        sys.exit(_pytest.main(self.pytest_args))


setup(
    name="notification-common-service",
    version=version,
    description="Notifcation common service package",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='django gizwits',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.8.1',
        'xinge-push==1.1.8.3',
        'boto3==1.4.4',
        'jpush==3.3.5',
    ],
    cmdclass={'test': pytest},
)
