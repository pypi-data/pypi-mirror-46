# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path, unlink, makedirs
from shutil import rmtree

__all__ = ['lock']

_builddir = path.join('.', 'build')

def lock(env):
	bdir = path.realpath(_builddir)
	bdir = path.join(bdir, env.profile(), env.name())
	env.log("build dir %s" % bdir)
	env.session.set('builddir', bdir)
	fn = path.normpath(bdir) + '.lock'
	env.debug("lock %s" % fn)
	env.session.set('lockfn', fn)
	try:
		fh = open(fn, 'x')
	except FileExistsError:
		raise env.error("lock file exists: %s" % fn)
	fh.write('1')
	fh.flush()
	fh.close()
	_initdir(env, bdir)

def unlock(env):
	fn = env.session.get('lockfn', default = None)
	if fn is None:
		env.debug('builddir not locked')
	else:
		env.debug("unlock %s" % fn)
		try:
			unlink(fn)
		except FileNotFoundError:
			raise env.error("unlock file not found: %s" % fn)

def _initdir(env, bdir):
	if path.exists(bdir):
		env.debug("rmtree %s" % bdir)
		rmtree(bdir)
	makedirs(bdir)

def _open(env, filename, mode = 'r'):
	builddir = env.session.get('builddir')
	fn = path.normpath(filename)
	if fn.startswith(path.sep):
		fn = fn.replace(path.sep, '', 1)
	fn = path.join(builddir, fn)
	if mode != 'r':
		dstdir = path.dirname(fn)
		env.debug("makedirs %s" % dstdir)
		makedirs(dstdir, exist_ok = True)
	env.debug("open(%s) %s" % (mode, fn))
	return open(fn, mode)

def create(env, filename):
	return _open(env, filename, mode = 'x')

def read(env, filename):
	return _open(env, filename, mode = 'r')

def write(env, filename, append = False):
	m = 'w'
	if append:
		m = 'a'
	return _open(env, filename, mode = m)
