#!/usr/bin/env bash

set -eux

export DISTRONODE_JINJA2_NATIVE=1
distronode-playbook runtests.yml -v "$@"
distronode-playbook --vault-password-file test_vault_pass test_vault.yml -v "$@"
distronode-playbook test_hostvars.yml -v "$@"
distronode-playbook nested_undefined.yml -v "$@"
distronode-playbook test_preserving_quotes.yml -v "$@"
unset DISTRONODE_JINJA2_NATIVE
