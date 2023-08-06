#!/bin/sh -eu

ENVDIR=${1:-'/opt/venv/pysadmdev'}
PIP=${ENVDIR}/bin/pip

python3 -m venv --prompt sadmdev --clear ${ENVDIR}

${PIP} install -r requirements-dev.txt --upgrade
${PIP} install -r requirements-test.txt --upgrade
${PIP} install -r requirements.txt --upgrade
${PIP} install -e .

${PIP} list
exit 0
