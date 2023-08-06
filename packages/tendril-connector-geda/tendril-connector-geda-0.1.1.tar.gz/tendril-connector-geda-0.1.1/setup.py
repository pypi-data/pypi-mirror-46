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
    'arrow',
    'tendril-config>=0.1.7',
    'tendril-identity>=0.1.7',
    'tendril-utils-core>=0.1.13',
    'tendril-utils-types>=0.1.8',
    'tendril-utils-vcs>=0.1.1',
    'tendril-utils-pdf>=0.1.1',
    'tendril-utils-gschem-files>=0.1.1',
    'tendril-conventions-electronics>=0.1.1',
    'tendril-eda>=0.1.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tendril-connector-geda',
    version='0.1.1',
    description="gEDA interface connector for tendril",
    long_description=readme,
    author="Chintalagiri Shashank",
    author_email='shashank@chintal.in',
    url='https://github.com/chintal/tendril-connector-geda',
    packages=find_packages(),
    install_requires=requirements,
    license="AGPLv3",
    zip_safe=False,
    keywords='tendril',
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    # test_suite='tests',
    # tests_require=test_requirements
)
