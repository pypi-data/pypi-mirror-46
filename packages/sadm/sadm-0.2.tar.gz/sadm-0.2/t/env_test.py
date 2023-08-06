# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises
from os import path
from time import time

from _sadm import asset
from _sadm.env import Env, _lock, _unlock
from _sadm.env.profile import Profile
from _sadm.env.settings import Settings
from _sadm.errors import EnvError

def test_env(testing_env):
	e = testing_env()
	assert isinstance(e, Env)
	assert e._cfgfile == 'config.ini'
	assert e.name() == 'testing'
	assert isinstance(e._profile, Profile)
	assert e._profile.name() == 'testing'
	assert isinstance(e.assets, asset.Manager)
	# ~ e.configure()
	assert isinstance(e.settings, Settings)

def test_env_error(testing_env):
	with raises(EnvError, match = 'env not found'):
		Env('testing', 'noenv')
	e = testing_env()
	e._cfgfile = ''
	with raises(EnvError, match = 'config file not set'):
		e._loadcfg()

def test_load_error(testing_env):
	e = testing_env()
	with raises(EnvError, match = 'config file not set'):
		e._load(fn = '')
	with raises(EnvError, match = 'testing profile dir not set'):
		e._load(pdir = '')

def test_start_end_action(testing_env):
	e = testing_env()
	assert [n for n in e._run.keys()] == []
	e.start('testing_action')
	assert [n for n in e._run.keys()] == ['testing_action']
	assert e._run['testing_action'].get('start', '') != ''
	assert e._run['testing_action'].get('tag.prev', None) is not None
	assert e._run['testing_action'].get('end', None) is None
	e.end('testing_action')
	assert e._run['testing_action'].get('end', '') != ''

def test_start_end_error(testing_env):
	e = testing_env()
	assert [n for n in e._run.keys()] == []
	e.start('testing_error')
	with raises(EnvError, match = 'testing_error action already started'):
		e.start('testing_error')
	assert [n for n in e._run.keys()] == ['testing_error']
	with raises(EnvError, match = 'testing_end_error action was not started'):
		e.end('testing_end_error')

def test_report(testing_env):
	e = testing_env()
	e.start('action1')
	e.end('action1')
	e.report('testing_report')
	e.report('testing_report', startTime = time() - 10)
	e.start('action2')
	with raises(EnvError, match = 'not finished action\(s\): action2'):
		e.report('testing_report')

def test_lock(testing_env):
	fn = path.join('tdata', 'testing', 'sadm.lock')
	e = testing_env()
	with e.lock():
		assert e._lockfn.endswith(fn)
		assert path.isfile(fn)
	assert not path.isfile(fn)
	assert e._lockfn is None

def test_lock_error(testing_env):
	fn = path.join('tdata', 'testing', 'sadm.lock')
	e = testing_env()
	_lock(e)
	assert path.isfile(fn)
	with raises(EnvError, match = 'lock file exists:'):
		_lock(e)
	_unlock(e)
	assert not path.isfile(fn)

def test_unlock_error(testing_env):
	fn = path.join('tdata', 'testing', 'sadm.lock')
	e = testing_env()
	_lock(e)
	assert path.isfile(fn)
	assert e._lockfn is not None
	_unlock(e)
	assert not path.isfile(fn)
	assert e._lockfn is None
	_unlock(e)
	assert e._lockfn is None
	e._lockfn = fn
	with raises(EnvError, match = 'unlock file not found:'):
		_unlock(e)
	assert not path.isfile(fn)
