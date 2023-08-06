# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from contextlib import contextmanager
from os import path, unlink
from time import time

from _sadm import log, config, asset
from _sadm.configure import plugins
from _sadm.env import cmd
from _sadm.env.profile import Profile
from _sadm.env.session import Session
from _sadm.env.settings import Settings
from _sadm.errors import Error, EnvError

__all__ = ['Env', 'run']

class Env(object):
	_name = None
	_cfgfile = None
	_profile = None
	_profName = None
	_logtag = None
	_run = None
	_lockfn = None
	assets = None
	settings = None
	session = None

	def __init__(self, profile, name):
		self._name = name
		self._profile = Profile(profile)
		self._profName = self._profile.name()
		self._logtag = ''
		self._run = {}
		self.settings = Settings()
		self.session = Session()
		self._load()

	def _load(self, fn = None, pdir = None):
		# env config.ini
		opt = "env.%s" % self._name
		if fn is None:
			fn = config.get(self._profName, opt, fallback = None)
			if fn is None:
				raise self.error('env not found')
		fn = path.normpath(fn.strip())
		if fn == '.':
			raise self.error('config file not set')
		self._cfgfile = fn
		# profile dir
		if pdir is None:
			pdir = config.get(self._profName, 'dir', fallback = '.')
		pdir = path.normpath(pdir.strip())
		if not path.exists(pdir):
			raise self.error("%s directory not found" % pdir)
		if not path.isdir(pdir):
			raise self.error("%s is not a directory" % pdir)
		# env assets
		_rootdir = path.realpath(pdir)
		self.assets = asset.Manager(_rootdir)
		self.debug("assets %s" % _rootdir)

	def configure(self):
		self.debug('session start')
		self.session.start()
		try:
			plugins.configure(self)
		except FileNotFoundError as err:
			raise self.error("%s" % err)

	def name(self):
		return self._name

	def profile(self):
		return self._profName

	def cfgfile(self):
		return self._cfgfile

	def _log(self, func, msg):
		func("%s/%s%s %s" % (self._profName, self._name, self._logtag, msg))

	def log(self, msg):
		self._log(log.msg, msg)

	def info(self, msg):
		self._log(log.info, msg)

	def warn(self, msg):
		self._log(log.warn, msg)

	def debug(self, msg):
		tag = "%s/%s%s" % (self._profName, self._name, self._logtag)
		log.debug("%s" % msg, depth = 4, tag = tag)

	def error(self, msg):
		self._log(log.error, msg)
		return EnvError(msg)

	def start(self, action, msg = ''):
		if self._run.get(action, None) is not None:
			raise self.error("%s action already started" % action)
		prev = self._logtag
		self._logtag = " %s" % action
		sep = ''
		if msg != '':
			sep = ' '
		self.info("start%s%s" % (sep, msg))
		self._run[action] = {'tag.prev': prev, 'start': time()}

	def end(self, action):
		if self._run.get(action, None) is None:
			raise self.error("%s action was not started" % action)
		self._run[action]['end'] = time()
		self.info("end (%fs)" % (self._run[action]['end'] - self._run[action]['start']))
		self._logtag = self._run[action]['tag.prev']

	def report(self, action, startTime = None):
		actno = 0
		noend = []
		for n, d in self._run.items():
			actno += 1
			if d.get('end', None) is None:
				noend.append(n)
		took = ''
		if startTime is not None:
			took = " in %f seconds" % (time() - startTime)
		self.info("%s %d/%d actions%s" % (action, (actno - len(noend)), actno, took))
		if len(noend) > 0:
			raise self.error("not finished action(s): %s" % ','.join(noend))

	@contextmanager
	def lock(self):
		try:
			yield _lock(self)
		finally:
			_unlock(self)

def run(profile, env, action):
	try:
		env = Env(profile, env)
		cmd.run(env, action)
	except EnvError:
		return 1
	except Error as err: # pragma: no cover
		log.error("%s" % err)
		return 2
	return 0

def _lock(env):
	fn = path.join(env.assets.rootdir(), path.dirname(env.cfgfile()), '.lock')
	env.debug("lock %s" % fn)
	try:
		fh = open(fn, 'x')
	except FileExistsError:
		raise env.error("lock file exists: %s" % fn)
	fh.write('1')
	fh.flush()
	fh.close()
	env._lockfn = fn
	return env

def _unlock(env):
	if env._lockfn is None:
		env.debug('unlock env: not locked')
	else:
		env.debug("unlock %s" % env._lockfn)
		try:
			unlink(env._lockfn)
		except FileNotFoundError:
			raise env.error("unlock file not found: %s" % env._lockfn)
		finally:
			env._lockfn = None
