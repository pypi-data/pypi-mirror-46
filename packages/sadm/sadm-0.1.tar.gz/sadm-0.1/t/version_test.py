# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import version

def test_get():
	v = version.get()
	assert isinstance(v, str)

def test_string():
	v = version.string()
	assert isinstance(v, str)
	assert v.startswith('%(prog)s version ')
