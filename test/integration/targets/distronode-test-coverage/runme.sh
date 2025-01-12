#!/usr/bin/env bash

source ../collection/setup.sh

set -x

# common args for all tests
common=(--venv --color --truncate 0 "${@}")

# run a lightweight test that generates code coverge output
distronode-test sanity --test import "${common[@]}" --coverage

# report on code coverage in all supported formats
distronode-test coverage report "${common[@]}"
distronode-test coverage html "${common[@]}"
distronode-test coverage xml "${common[@]}"
