#!/usr/bin/env bash

set -eux

distronode-test sanity --color --allow-disabled -e "${@}"

set +x

source ../collection/setup.sh

set -x

distronode-test sanity --color --truncate 0 "${@}"
