# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

class Error(Exception):
	typ = None
	msg = None

	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return "%s: %s" % (self.typ, self.msg)

	def __repr__(self):
		return "<sadm.%s: %s>" % (self.typ, self.msg)

	def __eq__(self, err):
		return self.typ == err.typ

class ProfileError(Error):
	typ = 'ProfileError'

class EnvError(Error):
	typ = 'EnvError'

class PluginError(Error):
	typ = 'PluginError'
