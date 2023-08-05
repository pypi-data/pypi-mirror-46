# -*- encoding: utf-8 -*-

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import sys

def _getPrefixIdx():
	inf = sys._getframe(0)
	idx = inf.f_code.co_filename.find('pysadm')
	if idx <= 0:
		return 0
	return idx + 7

_idx = _getPrefixIdx()

def _getCaller(depth = 2):
	inf = sys._getframe(depth)
	return "%s:%d" % (inf.f_code.co_filename[_idx:], inf.f_lineno)

def debug(msg, *args):
	print('D:', _getCaller(), msg, *args, file = sys.stderr)

def error(msg, *args):
	print('E:', msg, *args, file = sys.stderr)

def info(msg, *args):
	print('I:', msg, *args, file = sys.stderr)

def msg(msg, *args):
	print(msg, *args, file = sys.stdout)
