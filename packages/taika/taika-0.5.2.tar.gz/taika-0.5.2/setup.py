#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages
from setuptools import setup

with open("README.rst") as readme_file:
    README = readme_file.read()

with open("HISTORY.rst") as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = ["ruamel.yaml", "docutils", "jinja2", "beautifulsoup4"]

SETUP_REQUIREMENTS = ["pytest-runner"]

TEST_REQUIREMENTS = ["pytest"]

setup(
    author="Hector Martinez-Lopez",
    author_email="hector.martinez.ub@gmail.com",
    maintainer="Hector Martinez-Lopez",
    maintainer_email="hector.martinez.ub@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    description="Another Static Site Generator",
    entry_points={"console_scripts": ["taika=taika.cli:main"]},
    install_requires=REQUIREMENTS,
    license="MIT license",
    long_description=README + "\n\n" + HISTORY,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="taika",
    name="taika",
    packages=find_packages(include=["*"]),
    setup_requires=SETUP_REQUIREMENTS,
    py_requires=">=3.6",
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://gitlab.com/hectormartinez/taika",
    version="0.5.2",
    zip_safe=False,
)
