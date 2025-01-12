#!/usr/bin/env bash

set -ux
export DISTRONODE_BECOME_ALLOW_SAME_USER=1
export DISTRONODE_ROLES_PATH=../
distronode-playbook -i ../../inventory runme.yml -v "$@"
