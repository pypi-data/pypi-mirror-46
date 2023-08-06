# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import configure

_expectPlugins = {
	0: 'testing',
	1: 'sadm',
	2: 'sadmenv',
	3: 'os',
	4: 'os.user',
}

def test_plugins_list():
	idx = 0
	for p in configure.pluginsList():
		assert p == _expectPlugins[idx]
		idx += 1

def test_plugins_list_revert():
	idx = max(_expectPlugins.keys())
	for p in configure.pluginsList(revert = True):
		assert p == _expectPlugins[idx]
		idx -= 1
