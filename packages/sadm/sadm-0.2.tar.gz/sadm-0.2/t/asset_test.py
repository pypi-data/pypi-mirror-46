# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises
from os import path, makedirs, unlink

from io import UnsupportedOperation
from os import path

from _sadm.asset import Manager

_rootdir = path.join('tdata', 'testing')

def test_manager():
	m = Manager(_rootdir)
	assert m._dir.endswith(_rootdir)
	with m.open('asset.test') as fh:
		fh.close()
	with raises(FileNotFoundError):
		m.open('nofile')

def test_read_only():
	rdir = path.join('tdata', 'tmp')
	fn = path.join(rdir, 'asset-readonly.test')
	if path.isfile(fn):
		unlink(fn)
	makedirs(rdir, exist_ok = True)
	with open(fn, 'x') as fh:
		fh.write('testing')
	assert path.isfile(fn)
	m = Manager(rdir)
	with raises(UnsupportedOperation, match = 'not writable'):
		with m.open('asset-readonly.test') as fh:
			fh.write('testing')
	unlink(fn)
