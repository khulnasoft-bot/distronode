#!/usr/bin/env bash

set -eux

DISTRONODE_INVENTORY_ENABLED=notyaml distronode-playbook subdir/play.yml -i notyaml.yml "$@"
