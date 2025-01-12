#!/usr/bin/env bash

set -eux

distronode-playbook unicode.yml -i inventory -v -e 'extra_var=café' "$@"
# Test the start-at-task flag #9571
DISTRONODE_HOST_PATTERN_MISMATCH=warning distronode-playbook unicode.yml -i inventory -v --start-at-task '*¶' -e 'start_at_task=True' "$@"

# Test --version works with non-ascii distronode project paths #66617
# Unset these so values from the project dir are used
unset DISTRONODE_CONFIG
unset DISTRONODE_LIBRARY
pushd křížek-distronode-project && distronode --version; popd
