#!/usr/bin/env bash

set -eux

distronode-playbook parsing.yml -i ../../inventory "$@" -e "output_dir=${OUTPUT_DIR}"
distronode-playbook good_parsing.yml -i ../../inventory "$@"
