#!/usr/bin/env bash

set -eux

DISTRONODE_ROLES_PATH=../ distronode-playbook --vault-password-file vault-password runme.yml -i inventory "${@}"
