# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import pytest
from os import path, makedirs

# logger

from _sadm import log
log._colored = False

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
	def wrapper(profile = 'testing', env = 'testing'):
		e = envmod.Env(profile, env)
		e.configure()
		return e.settings
	return wrapper
