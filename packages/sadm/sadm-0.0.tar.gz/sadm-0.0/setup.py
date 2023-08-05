#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import sys
from os import path
from setuptools import setup, find_packages

def cat(fpath):
	with open(fpath, 'r') as fh:
		return fh.read()

desc = 'sysadmin/devops/deploy tools'
long_desc = cat('README.md')
version = cat('VERSION').strip()

install_requires = []

setup(
	name = 'sadm',
	version = version,
	description = desc,
	long_description = long_desc,
	long_description_content_type = 'text/markdown',
	license = 'BSD',
	url = 'https://github.com/jrmsdev/pysadm',
	author = 'Jeremías Casteglione',
	author_email = 'jrmsdev@gmail.com',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python :: 3',
		'Operating System :: POSIX :: Linux',
	],
	packages = find_packages(),
	install_requires = install_requires,
	zip_safe = False,
	test_suite = 'test.suite',
)
