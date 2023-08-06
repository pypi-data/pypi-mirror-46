#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

# https://packaging.python.org/guides/distributing-packages-using-setuptools/

from setuptools import setup, find_packages

def main():

	with open('requirements.txt', 'r') as fh:
		deps = fh.read().splitlines()

	setup(
		python_requires = '~=3.4',
		setup_requires = ['setuptools_scm>=3.3'],
		install_requires = deps,
		use_scm_version = {'write_to': '_sadm/_version.py'},
		py_modules = ['sadm'],
		packages = find_packages(),
		include_package_data = True,
	)

if __name__ == '__main__':
	main()
