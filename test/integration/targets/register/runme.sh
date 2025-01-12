#!/usr/bin/env bash

set -eux

# does it work?
distronode-playbook can_register.yml -i ../../inventory -v "$@"

# ensure we continue when distronode-playbook errors out
set +e
result="$(distronode-playbook invalid.yml -i ../../inventory -v "$@" 2>&1)"
set -e
grep -q "Invalid variable name in " <<< "${result}"
