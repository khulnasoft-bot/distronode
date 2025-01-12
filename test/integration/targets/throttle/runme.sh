#!/usr/bin/env bash

set -eux

# https://github.com/distronode/distronode/pull/42528
SELECTED_STRATEGY='linear' distronode-playbook test_throttle.yml -vv -i inventory --forks 12 "$@"
SELECTED_STRATEGY='free' distronode-playbook test_throttle.yml -vv -i inventory --forks 12 "$@"
