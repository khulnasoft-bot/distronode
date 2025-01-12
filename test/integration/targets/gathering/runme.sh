#!/usr/bin/env bash

set -eux

DISTRONODE_GATHERING=smart distronode-playbook smart.yml --flush-cache -i ../../inventory -v "$@"
DISTRONODE_GATHERING=implicit distronode-playbook implicit.yml --flush-cache -i ../../inventory -v "$@"
DISTRONODE_GATHERING=explicit distronode-playbook explicit.yml --flush-cache -i ../../inventory -v "$@"
