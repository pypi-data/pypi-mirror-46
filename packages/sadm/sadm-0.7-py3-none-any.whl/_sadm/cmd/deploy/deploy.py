# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import log

def cmdArgs(parser):
	p = parser.add_parser('deploy', help = 'deploy sadm.env')
	p.set_defaults(command = 'deploy')

def main(args):
	log.debug("deploy %s/%s" % (args.profile, args.env))
	return 128
