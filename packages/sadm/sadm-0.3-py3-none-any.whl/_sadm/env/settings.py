# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser

from _sadm.configure import pluginsList, getPlugin

__all__ = ['Settings']

class Settings(ConfigParser):

	def __init__(self):
		super().__init__(defaults = {}, allow_no_value = False, delimiters = ('=',),
			comment_prefixes = ('#',), strict = True, default_section = 'default')

	def plugins(self, action, revert = False):
		for p in pluginsList(revert = revert):
			if self.has_section(p):
				yield (p, getPlugin(p, action))
