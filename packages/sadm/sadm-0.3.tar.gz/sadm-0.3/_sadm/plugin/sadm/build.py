# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path, makedirs, unlink

_builddir = path.join('.', 'build')

def pre_build(env):
	env.debug('pre_build')
	makedirs(path.realpath(_builddir), exist_ok = True)
	env.log("build dir %s" % _builddir)
	_lock(env)

def _lock(env):
	lockfn = path.join(_builddir, env.profile(), env.name(), '.lock')
	env.debug("lockfn %s" % lockfn)
	env.session.set('lockfn', lockfn)
	try:
		fh = open(lockfn, 'x')
		fh.write('1')
		fh.flush()
		fh.close()
	except FileExistsError as err:
		raise env.error("%s" % err)

def build(env):
	env.debug('build')

def post_build(env):
	env.debug('post_build')
	_saveSession(env)
	_writeSettings(env)
	_unlock(env)

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

def _saveSession(env):
	fn = path.join(_builddir, env.profile(), env.name(), 'session.json')
	env.log("save %s" % fn)
	fn = path.realpath(fn)
	if path.isfile(fn):
		unlink(fn)
	env.session.dump(fn)

def _unlock(env):
	lockfn = env.session.get('lockfn')
	env.debug("lockfn %s" % lockfn)
	try:
		unlink(lockfn)
	except FileNotFoundError as err:
		raise env.error("%s" % err)
