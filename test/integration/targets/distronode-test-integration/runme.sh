#!/usr/bin/env bash

source ../collection/setup.sh

set -x

distronode-test integration --venv --color --truncate 0 "${@}"
