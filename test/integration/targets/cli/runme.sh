#!/usr/bin/env bash

set -eux

DISTRONODE_ROLES_PATH=../ distronode-playbook setup.yml

python test-cli.py

distronode-playbook test_syntax/syntax_check.yml --syntax-check -i ../../inventory -v "$@"
