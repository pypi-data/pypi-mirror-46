#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import sys
from os import path
from io import open


DESCRIPTION = ("Associates route53 PTR records to particular vpc.")
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

VERSION = '0.1.2'

setup_requires = (
    ['pytest-runner'] if any(x in sys.argv for x in ('pytest', 'test', 'ptr')) else []
)

setup(
    name='r53_ptr_vpc_associator',
    version=VERSION,
    description=DESCRIPTION,
    author='Will Rubel',
    author_email='willrubel@gmail.com',
    url='https://github.com/rubelw/r53_ptr_vpc_associator',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=setup_requires,
    tests_require=['pytest','mock'],
    test_suite="r53_ptr_vpc_associator.tests",
    data_files=[('make_lambda_zip.sh')],
    install_requires=[
        "boto3>=1.4.3",
        "requests>=2.18",
        "Click>=6.7",
        "configparser>=3.5.0",
        "future>=0.16.0",
        "six>=1.11.0",
        "coverage==4.0.3",
        "pip"
    ],
    keywords=['aws', 'route53', 'vpc'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points="""
        [console_scripts]
        associator=r53_ptr_vpc_associator.command:cli
    """
)