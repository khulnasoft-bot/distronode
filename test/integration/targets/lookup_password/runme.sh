#!/usr/bin/env bash

set -eux

source virtualenv.sh

DISTRONODE_ROLES_PATH=../ distronode-playbook runme.yml -e "output_dir=${OUTPUT_DIR}" "$@"
