# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from importlib import import_module
from os import path
from pytest import raises

from _sadm import configure
from _sadm.errors import PluginError

_expectPlugins = {
	0: 'testing',
	1: 'sadm',
	2: 'os',
}

def test_registered_plugins():
	assert configure._order == _expectPlugins

def test_register_error():
	with raises(RuntimeError, match = 'plugin testing already registered'):
		configure.register('testing', 'filename')

def test_plugins_list():
	idx = 0
	for p in configure.pluginsList():
		assert p == _expectPlugins[idx]
		idx += 1

def test_plugin_init():
	fn = configure.pluginInit('testing')
	assert fn.endswith(path.join('_sadm', 'plugin', 'testing', 'config.ini'))

def test_get_plugin():
	mod = configure.getPlugin('testing', 'configure')
	assert mod == import_module('_sadm.plugin.testing.configure')

def test_get_plugin_error():
	with raises(PluginError, match = 'noplugin plugin not found'):
		configure.getPlugin('noplugin', 'configure')
	with raises(PluginError, match = 'testing plugin nomod not implemented'):
		configure.getPlugin('testing', 'nomod')
