#!/usr/bin/env bash

source virtualenv.sh
export DISTRONODE_ROLES_PATH=../
set -euvx

distronode-playbook test.yml "$@"
