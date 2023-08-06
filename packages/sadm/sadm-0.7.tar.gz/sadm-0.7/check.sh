#!/bin/sh -eu
check-manifest
python3 setup.py check
python3 setup.py egg_info
pytest $@
exit 0
