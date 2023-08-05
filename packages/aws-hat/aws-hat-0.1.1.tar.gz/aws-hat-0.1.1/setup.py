# -*- coding: utf-8 -*-


'''setup.py: setuptools control.'''


import re
import setuptools
from os import path

version = "0.1.1"

setuptools.setup(
    name='aws-hat',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['hat = aws_hat.main:default']
    },
    version=version,
    description='Assume a role',
    long_description='Hat assumes a role and outputs temporary access keys',
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['boto3', 'requests', 'configparser', 'click'],
    author='Martijn van Dongen',
    author_email='martijnvandongen@binx.io',
    url='https://github.com/binxio/aws-hat',
)
