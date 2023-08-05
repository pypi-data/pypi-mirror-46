#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


requirements = ['loguru']

setup_requirements = []

test_requirements = []

setup(
    author="Adham Ehab",
    author_email='adhaamehab7@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Usain is native fast lightweight task runner framework",
    install_requires=requirements,
    license="MIT license",
    long_description="Usain is a native task runner and background jobs scheduler \n\n check out the repo for more info github.com/adhaamehab/usain",
    include_package_data=True,
    keywords='usain',
    name='usain',
    packages=find_packages(include=['usain']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/adhaamehab/usain',
    version='0.2.0',
    zip_safe=False,
)
