# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser
from _sadm import _cfg as cfg

cfg._readFiles = []

def test_cfg():
	c = cfg.new()
	assert isinstance(c, ConfigParser)
	assert len(c.defaults()) == 2
	assert len(c.sections()) == 0
