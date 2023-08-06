#!/bin/sh -eu
check-manifest
python3 setup.py check
pytest
exit 0
