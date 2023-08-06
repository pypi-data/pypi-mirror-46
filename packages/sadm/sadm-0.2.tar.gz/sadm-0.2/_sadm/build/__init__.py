# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

def run(env):
	for p, mod in env.settings.plugins('build'):
		tag = "build.%s" % p
		env.start(tag)
		mod.build(env)
		env.end(tag)
