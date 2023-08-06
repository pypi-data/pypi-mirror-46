#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup
    find_packages = None


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'tendril-utils-core>=0.1.13',
    'tendril-config>=0.1.6',
    'tendril-schema>=0.1.6'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tendril-identity',
    version='0.1.8',
    description="Tendril Identity Management",
    long_description=readme,
    author="Chintalagiri Shashank",
    author_email='shashank@chintal.in',
    url='https://github.com/chintal/tendril-identity',
    packages=find_packages(),
    install_requires=requirements,
    license="AGPLv3",
    zip_safe=False,
    keywords='tendril',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    # test_suite='tests',
    # tests_require=test_requirements
)
