# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path
from _sadm.plugin.utils import builddir

__all__ = ['build']

def build(env):
	homedir = env.settings.get('os', 'home.dir')
	env.debug("os home dir %s" % homedir)
	for user in env.settings['os.user']:
		uid = env.settings.getint('os.user', user)
		# ~ env.log("%d %s" % (uid, user))
		_synchome(env, user, homedir)

def _synchome(env, user, homedir):
	cfgdir = env.session.get('os.user.config.dir')
	srcdir = path.join(cfgdir, user)
	dstdir = path.join(homedir, user)
	if env.assets.isdir(cfgdir, user):
		env.log("sync %s -> %s" % (srcdir, dstdir))
		builddir.sync(env, srcdir, dstdir)
