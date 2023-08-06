# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import getenv
from io import StringIO
from bottle import route, view

from _sadm import log, config
from _sadm.web import tpl

@route('/')
@view('index.html')
@tpl.data('home')
def index():
	log.debug("index")
	return {
		'cfgfile': config._fn,
		'cfg': _getCfg(),
		'user': getenv('USER', 'nouser'),
	}

def _getCfg():
	buf = StringIO()
	config.reload()
	config.write(buf)
	buf.seek(0, 0)
	return buf.read()
