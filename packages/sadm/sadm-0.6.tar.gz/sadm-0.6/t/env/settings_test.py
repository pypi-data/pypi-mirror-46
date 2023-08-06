# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from pytest import raises

from _sadm.env.settings import Settings
from _sadm.errors import SettingsError

def test_settings(testing_env):
	env = testing_env()
	assert isinstance(env.settings, Settings)
	assert isinstance(env.settings, ConfigParser)

def test_plugins(testing_settings):
	s = testing_settings()
	assert sorted([p[0] for p in s.plugins('configure')]) == ['os', 'sadm', 'testing']

def test_parsing_error(testing_settings):
	with raises(SettingsError, match = 'Source contains parsing errors: '):
		testing_settings(cfgfile = 'config-parsing-error.ini')

def test_getlist_fallback(testing_settings):
	s = testing_settings()
	l = s.getlist('testing', 'test.notset.list', fallback = None)
	assert l is None
	with raises(SettingsError,
		match = 'No option \'test.notset.list\' in section: \'testing\''):
		s.getlist('testing', 'test.notset.list')

def test_getlist(testing_settings):
	s = testing_settings(cfgfile = 'config-settings-getlist.ini')
	l = s.getlist('testing', 'test.list.empty')
	assert isinstance(l, tuple)
	assert len(l) == 0

def test_getlist_comma(testing_settings):
	s = testing_settings(cfgfile = 'config-settings-getlist.ini')
	l = s.getlist('testing', 'test.list.comma')
	assert l == ('v0', 'v1', 'v2', 'v3')

def test_getlist_order(testing_settings):
	s = testing_settings(cfgfile = 'config-settings-getlist.ini')
	l = s.getlist('testing', 'test.list.order')
	assert l == ('v1', 'v3', 'v2', 'v0')

def test_getlist_lines(testing_settings):
	s = testing_settings(cfgfile = 'config-settings-getlist.ini')
	l = s.getlist('testing', 'test.list.lines')
	assert l == ('v0', 'v1', 'v2', 'v3')

def test_getlist_combined(testing_settings):
	s = testing_settings(cfgfile = 'config-settings-getlist.ini')
	l = s.getlist('testing', 'test.list.combined')
	assert l == ('v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6')
