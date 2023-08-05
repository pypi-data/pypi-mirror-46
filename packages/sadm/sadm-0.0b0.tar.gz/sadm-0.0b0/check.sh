#!/bin/sh -eu
check-manifest
python3 setup.py check -m -s
pytest
exit 0
