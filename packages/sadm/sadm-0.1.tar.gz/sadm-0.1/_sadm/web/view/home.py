# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from io import StringIO
from bottle import route, view

from _sadm import log
from _sadm import _cfg as cfg
from _sadm.web import tpl

@route('/')
@view('index.html')
@tpl.data('home')
def index():
	log.debug("index")
	return {
		'cfgfile': cfg._cfgFile,
		'cfg': _getCfg(),
	}

def _getCfg():
	buf = StringIO()
	config = cfg.new()
	config.write(buf)
	buf.seek(0, 0)
	return buf.read()
