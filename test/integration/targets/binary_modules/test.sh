#!/usr/bin/env bash

set -eux

[ -f "${INVENTORY}" ]

DISTRONODE_HOST_KEY_CHECKING=false distronode-playbook download_binary_modules.yml -i "${INVENTORY}" -v "$@"
DISTRONODE_HOST_KEY_CHECKING=false distronode-playbook test_binary_modules.yml     -i "${INVENTORY}" -v "$@"
