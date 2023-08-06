# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path, makedirs, unlink

_builddir = path.join('.', 'build')

def build(env):
	env.debug(env.name())
	env.log("build dir %s" % _builddir)
	_writeSettings(env)

def _writeSettings(env):
	fn = path.join(_builddir, env.profile(), env.name(), 'configure.ini')
	freal = path.realpath(fn)
	dst = path.dirname(freal)
	makedirs(dst, exist_ok = True)
	if path.isfile(freal):
		unlink(freal)
	with open(freal, 'x') as fh:
		env.settings.write(fh)
	env.log("%s done" % fn)
