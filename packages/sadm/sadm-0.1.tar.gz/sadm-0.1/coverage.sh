#!/bin/sh -eu
python3 setup.py build
coverage run -m pytest $@
coverage report
coverage html
exit 0
