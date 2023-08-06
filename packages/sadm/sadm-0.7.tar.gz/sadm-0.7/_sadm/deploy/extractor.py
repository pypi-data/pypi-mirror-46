# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import json

from base64 import b64encode
from os import path, chmod

from _sadm import version, libdir
from _sadm.errors import BuildError

def gen(env):
	_vars = {
		'env': env.name(),
		'rootdir': path.join(path.sep, 'opt', 'sadm'),
	}
	cargo = {}
	n = path.normpath(env.build.rootdir())
	fn = n + '.deploy'
	env.log("%s.deploy" % env.name())
	for ext in ('.zip', '.env', '.env.asc'):
		name = n + ext
		if path.isfile(name):
			env.log("load %s" % path.basename(name))
			cargo[env.name() + ext] = _load(name)
		else:
			if ext != '.env.asc':
				raise BuildError("%s file not found" % name)
	_write(fn, cargo, _vars)

def _load(fn):
	with open(fn, 'rb') as fh:
		return b64encode(fh.read()).decode()

def _write(fn, cargo, _vars):
	sk = True
	indent = '\t'
	with libdir.openfile('deploy', 'build_extract.py') as src:
		with open(fn, 'x') as fh:
			for line in src.readlines():
				if line.startswith('_cargo'):
					fh.write("_cargo = %s\n" % json.dumps(cargo,
						indent = indent, sort_keys = sk))
				elif line.startswith('_vars'):
					fh.write("_vars = %s\n" % json.dumps(_vars,
						indent = indent, sort_keys = sk))
				else:
					fh.write(line)
			fh.write("\n# sadm version %s\n" % version.get())
			fh.flush()
	chmod(fn, 0o0500)
