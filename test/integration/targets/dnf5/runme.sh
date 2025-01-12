#!/usr/bin/env bash

set -ux
export DISTRONODE_ROLES_PATH=../
distronode-playbook playbook.yml "$@"
