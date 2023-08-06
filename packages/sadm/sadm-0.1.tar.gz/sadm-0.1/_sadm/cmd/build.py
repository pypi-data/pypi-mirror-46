# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import log
from _sadm.cmd import flags

def _getArgs():
	parser = flags.new('sadm-build', desc = 'build sadm profile data')
	parser.add_argument('cfgfile', help = 'path to config.json file')
	return flags.parse(parser)

def main():
	args = _getArgs()
	log.debug("cfgfile %s" % args.cfgfile)
	log.msg('done!')

if __name__ == '__main__':
	main()
