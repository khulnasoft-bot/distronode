#!/usr/bin/env bash

set -eux

distronode-playbook -i ../../inventory runme.yml -v "$@"

# https://github.com/distronode/distronode/issues/80710
DISTRONODE_REMOTE_TMP=./distronode distronode-playbook -i ../../inventory test_relative_tmp_dir.yml -v "$@"
