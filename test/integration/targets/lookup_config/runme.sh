#!/usr/bin/env bash

set -eux

DISTRONODE_ROLES_PATH=../ DISTRONODE_LOOKUP_PLUGINS=. distronode-playbook runme.yml "$@"
