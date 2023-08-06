# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from hashlib import sha256
from _sadm.plugin.utils import builddir

__all__ = ['pre_build', 'post_build']

def pre_build(env):
	builddir.lock(env)
	_writeSettings(env)

def post_build(env):
	_saveSession(env)
	builddir.unlock(env)

def _saveSession(env):
	env.log('session.json')
	with builddir.create(env, 'session.json', meta = True) as fh:
		env.session.dump(fh)

def _writeSettings(env):
	env.log('configure.ini')
	fn = None
	with builddir.create(env, 'configure.ini', meta = True) as fh:
		env.settings.write(fh)
		fn = fh.name
	h = sha256()
	with open(fn, 'rb') as fh:
		h.update(fh.read())
	env.session.set('sadm.configure.checksum', h.hexdigest())
