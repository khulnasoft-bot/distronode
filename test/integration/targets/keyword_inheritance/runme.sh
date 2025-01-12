#!/usr/bin/env bash

set -eux

DISTRONODE_ROLES_PATH=../ distronode-playbook -i ../../inventory test.yml "$@"

DISTRONODE_ROLES_PATH=../ distronode-playbook -i ../../inventory dep_keyword_inheritance.yml "$@"
