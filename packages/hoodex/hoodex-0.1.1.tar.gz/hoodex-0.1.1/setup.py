#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

def read_file(filepath):
    with open(filepath) as f:
        return f.read()

requirements = read_file('requirements.txt').splitlines()

setup_requirements = read_file('requirements_dev.txt').splitlines()

setup(
    author="Ratxi",
    author_email='ratxi.com@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Hoodex checks your plex instance and get the url of the latest uploaded content",
    entry_points={
        'console_scripts': [
            'hoodex=hoodex.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='hoodex',
    name='hoodex',
    packages=find_packages(include=['hoodex']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=setup_requirements,
    url='https://github.com/Ratxi/hoodex',
    version='0.1.1',
    zip_safe=False,
)
