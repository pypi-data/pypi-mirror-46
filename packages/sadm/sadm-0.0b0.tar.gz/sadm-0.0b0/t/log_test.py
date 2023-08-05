# -*- encoding: utf-8 -*-

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from sadm import log

def test_log():
	assert log._getCaller(1) == 't/log_test.py:9'
