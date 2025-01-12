#!/usr/bin/env bash
# Make sure that distronode-test continues to work when content config is invalid.

set -eu

source ../collection/setup.sh

set -x

distronode-test sanity --test import --python "${DISTRONODE_TEST_PYTHON_VERSION}" --color --venv -v
distronode-test units  --python "${DISTRONODE_TEST_PYTHON_VERSION}" --color --venv -v
distronode-test integration --color --venv -v
