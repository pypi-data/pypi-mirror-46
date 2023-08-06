# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path

class Manager(object):
	_dir = None

	def __init__(self, rootdir):
		self._dir = path.realpath(path.normpath(rootdir))

	def open(self, relname):
		return open(path.join(self._dir, path.normpath(relname)), 'r')
