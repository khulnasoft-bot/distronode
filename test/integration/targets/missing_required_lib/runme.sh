#!/usr/bin/env bash

set -eux
export DISTRONODE_ROLES_PATH=../
distronode-playbook -i ../../inventory runme.yml -e "output_dir=${OUTPUT_DIR}" -v "$@"
