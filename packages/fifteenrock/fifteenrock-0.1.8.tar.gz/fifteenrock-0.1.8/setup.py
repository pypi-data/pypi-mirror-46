#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'requests', 'pyrsistent', 'jupyter']

setup_requirements = []

test_requirements = []

setup(
    author="Rajiv Abraham",
    author_email='rajiv.abraham@15rock.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python client library for the 15Rock platform.",
    entry_points={
        'console_scripts': [
            'fifteenrock=fifteenrock.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fifteenrock',
    name='fifteenrock',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RAbraham/fifteenrock',
    version='0.1.8',
    zip_safe=False,
)
