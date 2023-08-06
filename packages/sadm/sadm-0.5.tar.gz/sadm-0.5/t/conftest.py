# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import pytest
from os import path, makedirs, unlink
from shutil import rmtree

# logger

from _sadm import log
log._colored = False
log.init('quiet')

# register testing plugin

import _sadm.plugin.testing

# config

from _sadm import cfg
cfg._cfgFile = path.join('tdata', 'sadm.cfg')

# attach testing config

import _sadm
del _sadm.config
_sadm.config = cfg.new()

# configure plugins testing

from _sadm.plugin.utils import builddir
builddir._builddir = path.join('tdata', 'builddir')
makedirs(path.join(builddir._builddir, 'testing', 'testing'), exist_ok = True)

# testing profile

from _sadm.env import profile

@pytest.fixture
def testing_profile():
	def wrapper(name = 'testing'):
		return profile.Profile(name)
	return wrapper

# testing env

from _sadm import env

@pytest.fixture
def testing_env():
	def wrapper(name = 'testing', profile = 'testing'):
		return env.Env(profile, name)
	return wrapper

# testing settings

@pytest.fixture
def testing_settings():
	envmod = env
	def wrapper(profile = 'testing', env = 'testing', cfgfile = None):
		if cfgfile is not None:
			cfgfile = path.join(profile, cfgfile)
		e = envmod.Env(profile, env)
		e.configure(cfgfile = cfgfile)
		return e.settings
	return wrapper

# testing env setup

from _sadm.env import cmd as envcmd

@pytest.fixture
def env_setup():
	def wrapper(name = 'testing', profile = 'envsetup',
		configure = False, cfgfile = None, action = None):
		if action is not None:
			configure = False # configure in called from cmd.run
		e = env.Env(profile, name)
		_cleanSetup(e)
		if configure:
			e.configure(cfgfile = cfgfile)
		if action is not None:
			envcmd.run(e, action)
		return e
	return wrapper

def _cleanSetup(env):
	en = env.name()
	_bdirs = [
		path.join('tdata', 'builddir', 'envsetup', en),
		path.join('tdata', 'builddir', 'envsetup', en + '.meta'),
	]
	for bdir in _bdirs:
		if path.isdir(bdir):
			rmtree(bdir)
	_bfiles = [
		path.join('tdata', 'builddir', 'envsetup', en + '.lock'),
		path.join('tdata', 'builddir', 'envsetup', en + '.zip'),
		path.join('tdata', 'builddir', 'envsetup', en + '.checksum'),
		path.join('tdata', 'setup', en, '.lock'),
	]
	for fn in _bfiles:
		if path.isfile(fn):
			unlink(fn)
