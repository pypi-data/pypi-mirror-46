# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.cmd import build as build_cmd
from _sadm.cmd import web as web_cmd

build = build_cmd.main
web = web_cmd.main

__all__ = ['build', 'web']
