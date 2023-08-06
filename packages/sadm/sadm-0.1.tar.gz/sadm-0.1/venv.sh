#!/bin/sh -eu

ENVDIR=${1:-'/opt/venv/pysadm'}
PIP=${ENVDIR}/bin/pip

python3 -m venv --prompt sadm --clear ${ENVDIR}

${PIP} install -r requirements.txt --upgrade
${PIP} install -e .

${PIP} list
exit 0
