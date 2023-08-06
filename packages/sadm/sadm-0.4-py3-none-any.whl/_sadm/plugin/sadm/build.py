# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.plugin.utils import builddir

__all__ = ['pre_build', 'build', 'post_build']

def pre_build(env):
	env.debug('pre_build')
	builddir.lock(env)

def build(env):
	env.debug('build')

def post_build(env):
	env.debug('post_build')
	_saveSession(env)
	_writeSettings(env)
	builddir.unlock(env)

def _saveSession(env):
	env.log('save session.json')
	with builddir.create(env, 'session.json') as fh:
		env.session.dump(fh)

def _writeSettings(env):
	with builddir.create(env, 'configure.ini') as fh:
		env.settings.write(fh)
	env.log('configure.ini done')
