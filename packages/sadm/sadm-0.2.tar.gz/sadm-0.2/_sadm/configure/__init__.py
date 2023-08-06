# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path
from importlib import import_module

try:
	# python >= 3.6
	importError = ModuleNotFoundError
except NameError: # pragma: no cover
	# python 3.4 and 3.5
	importError = Exception

from _sadm import log
from _sadm.errors import PluginError

__all__ = ['register', 'getPlugin', 'pluginInit', 'pluginList']

_reg = {}
_order = {}
_next = 0

def register(name, filename):
	global _next
	n = name.split('.')[-1]
	if _reg.get(n, None) is not None:
		raise RuntimeError("plugin %s already registered" % name)
	filename = path.realpath(path.normpath(filename))
	_reg[n] = {
		'name': name,
		'config': path.join(path.dirname(filename), 'config.ini'),
	}
	_order[_next] = n
	_next += 1

def pluginsList():
	for idx in sorted(_order.keys()):
		yield _order[idx]

def pluginInit(name, fn = None):
	if fn is None:
		fn = _reg[name]['config']
	return fn

def getPlugin(name, mod):
	p = _reg.get(name, None)
	if p is None:
		raise PluginError("%s plugin not found" % name)
	try:
		mod = import_module("%s.%s" % (p['name'], mod))
	except importError as err:
		log.debug("%s" % err)
		raise PluginError("%s plugin %s not implemented!" % (name, mod))
	return mod
