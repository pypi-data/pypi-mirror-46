# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import sys
from os import path, system, makedirs, unlink, chmod
from shutil import move

from _sadm import log

def loadenv(filename):
	envfn = path.realpath(filename)
	if path.isfile(envfn + '.asc'):
		rc = system("gpg --no-tty --no --verify %s.asc %s 2>/dev/null" % (envfn, envfn))
		if rc == 0:
			log.msg("%s: OK" % envfn)
		else:
			log.error('env signature verify failed!')
			return 1
	rc = system("sha256sum -c %s" % envfn)
	if rc != 0:
		log.error('env checksum failed!')
		return 2
	_importenv(envfn)
	return 0

def _importenv(envfn):
	basefn = envfn[:-4]
	rootdir = path.dirname(path.dirname(envfn))
	deploydir = path.join(rootdir, 'deploy')
	makedirs(deploydir, exist_ok = True)
	chmod(deploydir, 0o0700)
	for ext in ('.env', '.zip'):
		fn = basefn + ext
		dstfn = path.join(deploydir, path.basename(fn))
		if path.isfile(dstfn):
			unlink(dstfn)
		log.msg("%s: %s" % (fn, dstfn))
		move(fn, dstfn)
