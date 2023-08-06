# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.web import tpl

def test_loaded():
	assert tpl._viewreg == {
		'home': True,
		'syslog': True,
		'about': True,
	}, 'missing view'
