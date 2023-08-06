# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser

from _sadm.env.settings import Settings

def test_settings(testing_env):
	env = testing_env()
	assert isinstance(env.settings, Settings)
	assert isinstance(env.settings, ConfigParser)

def test_plugins(testing_settings):
	s = testing_settings()
	assert sorted([p[0] for p in s.plugins('configure')]) == ['os', 'sadm', 'testing']
