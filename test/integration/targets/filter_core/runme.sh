#!/usr/bin/env bash

set -eux

DISTRONODE_ROLES_PATH=../ distronode-playbook runme.yml "$@"
DISTRONODE_ROLES_PATH=../ distronode-playbook handle_undefined_type_errors.yml "$@"
