#!/usr/bin/env bash

set -eux

distronode-playbook -v -i inventory.ini test_distronode_become.yml

distronode-inventory -v -i inventory.ini --list 2> out
test "$(grep -c 'SyntaxWarning' out)" -eq 0
