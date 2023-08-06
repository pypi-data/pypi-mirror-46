# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import version

def configure(env, cfg):
	env.debug(env.name())
	s = env.settings
	s.set('sadm', 'version', version.get())
	s.set('sadm', 'env', env.name())
	s.set('sadm', 'profile', env.profile())
