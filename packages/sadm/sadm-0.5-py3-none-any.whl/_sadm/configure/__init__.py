# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from collections import deque, namedtuple
from importlib import import_module
from os import path

try:
	# python >= 3.6
	importError = ModuleNotFoundError
except NameError: # pragma: no cover
	# python 3.4 and 3.5
	importError = Exception

from _sadm import log
from _sadm.errors import PluginError

__all__ = ['register', 'getPlugin', 'pluginList']

_reg = {}
_order = deque()

Plugin = namedtuple('Plugin', ('name', 'fullname', 'config', 'meta', 'mod'))

def register(name, filename):
	global _next
	n = name.replace('_sadm.plugin.', '')
	if _reg.get(n, None) is not None:
		raise RuntimeError("plugin %s already registered" % name)
	filename = path.realpath(path.normpath(filename))
	cfgfn = path.join(path.dirname(filename), 'config.ini')
	metafn = path.join(path.dirname(filename), 'meta.json')
	_reg[n] = {
		'name': name,
		'config': cfgfn,
		'meta': metafn,
	}
	_order.append(n)

def pluginsList(revert = False):
	if revert:
		for p in reversed(_order):
			yield p
	else:
		for p in _order:
			yield p

def getPlugin(name, mod):
	p = _reg.get(name, None)
	if p is None:
		raise PluginError("%s plugin not found" % name)
	try:
		mod = import_module("%s.%s" % (p['name'], mod))
	except importError as err:
		log.debug("%s" % err)
		raise PluginError("%s plugin %s not implemented!" % (name, mod))
	return Plugin(name = name, fullname = p['name'],
		config = p['config'], meta = p['meta'], mod = mod)
