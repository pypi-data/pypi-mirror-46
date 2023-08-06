# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os.path import realpath, dirname, join

__all__ = ['path']

_srcdir = realpath(dirname(__file__))

def path(*args):
	return join(_srcdir, *args)
