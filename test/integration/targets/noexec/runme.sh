#!/usr/bin/env bash

set -eux

trap 'umount "${OUTPUT_DIR}/ramdisk"' EXIT

mkdir "${OUTPUT_DIR}/ramdisk"
mount -t tmpfs -o size=32m,noexec,rw tmpfs "${OUTPUT_DIR}/ramdisk"
DISTRONODE_REMOTE_TMP="${OUTPUT_DIR}/ramdisk" distronode-playbook -i inventory "$@" test-noexec.yml
