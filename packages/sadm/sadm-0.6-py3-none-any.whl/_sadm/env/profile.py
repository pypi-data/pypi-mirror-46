# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import log, config
from _sadm.errors import ProfileError

__all__ = ['Profile']

class Profile(object):
	_name = None

	def __init__(self, name):
		self._name = name
		self._load()

	def _load(self):
		log.debug("load %s" % self._name)
		if not config.has_section(self._name):
			log.debug("%s profile not found" % self._name)
			raise ProfileError("%s profile not found" % self._name)

	def name(self):
		return self._name
