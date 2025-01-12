#!/usr/bin/env bash

source ../collection/setup.sh

set -x

options=$("${TEST_DIR}"/../distronode-test/venv-pythons.py)
IFS=', ' read -r -a pythons <<< "${options}"

distronode-test units --color --truncate 0 "${pythons[@]}" "${@}"
