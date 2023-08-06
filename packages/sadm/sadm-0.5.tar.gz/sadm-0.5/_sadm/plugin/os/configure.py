# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import sys

def configure(env, cfg):
	sess = env.session
	sess.set('os.platform', sys.platform)
