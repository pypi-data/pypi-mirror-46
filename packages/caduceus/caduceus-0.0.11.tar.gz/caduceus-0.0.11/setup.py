#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

from setuptools.command.test import test as TestCommand

from caduceus import __version__

if sys.version_info < (3, 0):
    sys.exit("Sorry, Python 2 is not supported.")


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="caduceus",
    version=__version__,
    description="Caduceus notifies you if your scheduled tasks/cron jobs did not run.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Stavros Korokithakis",
    author_email="hi@stavros.io",
    url="https://gitlab.com/stavros/caduceus",
    packages=["caduceus"],
    package_dir={"caduceus": "caduceus"},
    install_requires=["apscheduler", "flask", "peewee", "requests", "toml", "schema", "pytimeparse"],
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
    python_requires=">3.4.0",
    license="MIT",
    keywords="caduceus tasks dead man switch notify",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite="tests",
    entry_points={"console_scripts": ["caduceus=caduceus.cli:main"]},
)
