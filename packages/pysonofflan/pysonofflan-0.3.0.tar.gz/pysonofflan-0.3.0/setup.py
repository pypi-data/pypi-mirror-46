#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'click_log', 'websockets']
setup_requirements = []
test_requirements = ['pytest', 'tox', 'python-coveralls']

setup(
    author="Andrew Beveridge",
    author_email='andrew@beveridge.uk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Interface for Sonoff devices running original Itead "
                "firmware, in LAN mode.",
    entry_points={
        'console_scripts': [
            'pysonofflan=pysonofflan.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pysonofflan',
    name='pysonofflan',
    packages=find_packages(include=['pysonofflan']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/beveradb/pysonofflan',
    version='0.3.0',
    zip_safe=False,
)
