# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import tarfile

from collections import deque
from os import path

from _sadm import asset
from _sadm.errors import BuildError

class Manager(asset.Manager):
	_tar = None
	_tarfn = None

	def create(self):
		rdir = self.rootdir()
		en = path.basename(rdir)
		mdir = path.normpath(rdir) + '.meta'
		self._tarfn = path.join(mdir, en + '.tar')
		# python 3.4 does not support 'x:' open mode
		# self._tar = tarfile.open(self._tarfn, 'x:')
		if path.isfile(self._tarfn):
			raise BuildError("%s file exists" % self._tarfn)
		self._tar = tarfile.open(self._tarfn, 'w')

	def close(self):
		if self._tar is not None:
			self._tar.close()

	def _tarinfo(self, inf, user = 'root', group = '',
		filemode = 0o0644, dirmode = 0o0755):
		if group == '':
			group = user
		inf.mtime = 0 # reproducible builds
		inf.uid = 0
		inf.gid = 0
		inf.uname = user
		inf.gname = group
		if inf.isdir():
			inf.mode = dirmode
		else:
			inf.mode = filemode

	def addfile(self, name, **kwargs):
		arcname = self.name(name)
		fn = path.join(self.rootdir(), arcname)
		fi = self._tar.gettarinfo(name = fn, arcname = arcname)
		self._tarinfo(fi, **kwargs)
		self._tar.addfile(fi)

	def adddir(self, name, **kwargs):
		def dirfilter(fi):
			self._tarinfo(fi, **kwargs)
			return fi
		arcname = self.name(name)
		dirpath = path.join(self.rootdir(), arcname)
		self._tar.add(dirpath, arcname = arcname, recursive = True,
			filter = dirfilter)
