# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import argparse

from _sadm import log, version, config

def new(prog, desc = ''):
	p = argparse.ArgumentParser(prog = prog, description = desc)
	p.add_argument('-V', '--version', help = 'show version and exit',
		action = 'version', version = version.string())
	p.add_argument('--debug', help = 'enable debug settings',
		action = 'store_true', default = False)
	p.add_argument('--log', help = 'set log level (error)',
		default = 'error', choices = log.levels())
	defenv = config.get('default', 'env')
	p.add_argument('--env', help = "env name (%s)" % defenv,
		metavar = 'name', default = defenv)
	defprof = config.get('default', 'profile')
	p.add_argument('--profile', help = "profile name (%s)" % defprof,
		metavar = 'name', default = defprof)
	return p

def parse(p):
	args = p.parse_args()
	if args.debug:
		log.init('debug')
	else:
		log.init(args.log)
	return args
