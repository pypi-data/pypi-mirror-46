# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from bottle import route, view

from _sadm import log, config
from _sadm.web import tpl

@route('/profile')
@view('profile.html')
@tpl.data('profile')
def index():
	log.debug('index')
	return {
		'profiles': _getallProfiles(),
	}

def _getallProfiles():
	config.reload()
	l = []
	for p in config.listProfiles():
		l.append(_getProfile(p))
	return l

def _getProfile(p):
	return {
		'name': p,
		'envs': config.listEnvs(p),
	}
