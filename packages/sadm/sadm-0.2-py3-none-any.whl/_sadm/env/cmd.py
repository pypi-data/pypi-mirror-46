# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from time import strftime, time

from _sadm import config, build
from _sadm.errors import EnvError

__all__ = ['run']

def run(env, action):
	_start = time()
	env.info("%s start %s" % (action, strftime('%c %z')))
	env.log("%s %s" % (config.name(), config.filename()))
	try:
		with env.lock() as env:
			env.configure()
			_run(env, action)
			env.report(action, startTime = _start)
	finally:
		env.info("%s end %s" % (action, strftime('%c %z')))

def _run(env, action):
	if action == 'build':
		build.run(env)
	else:
		raise EnvError("invalid action %s" % action)
