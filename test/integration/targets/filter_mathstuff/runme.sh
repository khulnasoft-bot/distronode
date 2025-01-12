#!/usr/bin/env bash

set -eux

export DISTRONODE_ROLES_PATH=../

distronode-playbook runme.yml "$@"
