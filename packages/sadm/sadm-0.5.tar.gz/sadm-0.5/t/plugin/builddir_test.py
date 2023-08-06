# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path, unlink
from pytest import raises

from _sadm.errors import SessionError, EnvError
from _sadm.plugin.utils import builddir

def test_builddir():
	bdir = path.join('tdata', 'builddir', 'testing', 'testing')
	assert path.isdir(bdir)

def test_lock_unlock(testing_env):
	lockfn = path.join('tdata', 'builddir', 'testing', 'testing.lock')
	env = testing_env()
	env.configure()
	assert not path.isfile(lockfn)
	builddir.lock(env)
	assert path.isfile(lockfn)
	builddir.unlock(env)
	assert not path.isfile(lockfn)

def test_lock_error(testing_env):
	lockfn = path.join('tdata', 'builddir', 'testing', 'testing.lock')
	env = testing_env()
	env.configure()
	assert not path.isfile(lockfn)
	builddir.lock(env)
	with raises(SessionError, match = 'builddir option already set'):
		builddir.lock(env)
	del env.session._d['builddir']
	del env.session._d['lockfn']
	with raises(EnvError, match = 'lock file exists: '):
		builddir.lock(env)
	builddir.unlock(env)

def test_unlock_error(testing_env):
	lockfn = path.join('tdata', 'builddir', 'testing', 'testing.lock')
	if path.isfile(lockfn):
		unlink(lockfn)
	env = testing_env()
	env.configure()
	assert not path.isfile(lockfn)
	with raises(SessionError, match = 'lockfn option not set'):
		builddir.unlock(env)
	builddir.lock(env) # set session lockfn
	builddir.unlock(env)
	with raises(EnvError, match = 'unlock file not found'):
		builddir.unlock(env)

def test_fpath(testing_env):
	env = testing_env()
	env.configure()
	builddir.lock(env)
	try:
		p = path.join('tdata', 'builddir', 'testing', 'testing', 'p1', 'p2', 'p3')
		assert builddir.fpath(env, 'p1', 'p2', 'p3') == path.realpath(p)
	finally:
		builddir.unlock(env)

def test_fpath_relname(testing_env):
	env = testing_env()
	env.configure()
	builddir.lock(env)
	try:
		p = path.join('tdata', 'builddir', 'testing', 'testing', 'p1', 'p2', 'p3')
		assert builddir.fpath(env, path.sep + 'p1', 'p2', 'p3') == path.realpath(p)
	finally:
		builddir.unlock(env)

def test_fpath_meta(testing_env):
	env = testing_env()
	env.configure()
	builddir.lock(env)
	try:
		p = path.join('tdata', 'builddir', 'testing', 'testing.meta', 'p1')
		assert builddir.fpath(env, 'p1', meta = True) == path.realpath(p)
	finally:
		builddir.unlock(env)

def test_create(testing_env):
	env = testing_env()
	env.configure()
	builddir.lock(env)
	try:
		fn = path.join('tdata', 'builddir', 'testing', 'testing', 'file.test')
		assert not path.isfile(fn)
		with builddir.create(env, 'file.test') as fh:
			fh.write('1')
		assert path.isfile(fn)
	finally:
		builddir.unlock(env)

def test_create_meta(testing_env):
	env = testing_env()
	env.configure()
	builddir.lock(env)
	try:
		fn = path.join('tdata', 'builddir', 'testing', 'testing.meta', 'file.test')
		assert not path.isfile(fn)
		with builddir.create(env, 'file.test', meta = True) as fh:
			fh.write('1')
		assert path.isfile(fn)
	finally:
		builddir.unlock(env)
