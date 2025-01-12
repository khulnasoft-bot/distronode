#!/usr/bin/env bash

set -eux

distronode-playbook test_group_by.yml -i inventory.group_by -v "$@"
DISTRONODE_HOST_PATTERN_MISMATCH=warning distronode-playbook test_group_by_skipped.yml -i inventory.group_by -v "$@"
