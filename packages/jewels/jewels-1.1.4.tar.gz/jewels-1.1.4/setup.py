#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
from os import path as os_path

# short/long description
short_desc = 'Secure file encryption and data access'
here = os_path.abspath(os_path.dirname(__file__))
try:
    with open(os_path.join(here,'README.md'),'r',encoding='utf-8') as f:
        long_desc = '\n' + f.read()
except FileNotFoundError:
    long_desc = short_desc

setup(
    name='jewels',
    version='1.1.4',
    description=short_desc,
    author='andrea capitanelli',
    author_email='andrea.capitanelli@gmail.com',
    maintainer='andrea capitanelli',
    maintainer_email='andrea.capitanelli@gmail.com',
    url='https://github.com/acapitanelli/jewels',
    install_requires=[
      'pycryptodome',
    ],
    packages=['jewels'],
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords='data file encryption aes256 eax cli',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography'
    ],
    scripts=[
        'bin/jewels-cli'
    ]
)
