#!/usr/bin/env bash

set -eux

DISTRONODE_COLLECTIONS_PATH="${PWD}/collection_root" distronode-playbook test.yml -i ../../inventory "$@"
