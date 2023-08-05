#!/bin/sh -eu
coverage run -m pytest
coverage report
coverage html
exit 0
