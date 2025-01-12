#!/usr/bin/env bash

set -eux

DISTRONODE_LOOKUP_PLUGINS=. DISTRONODE_ROLES_PATH=./ UNICODE_VAR=café distronode-playbook runme.yml "$@"

distronode-playbook template_lookup_vaulted/playbook.yml --vault-password-file template_lookup_vaulted/test_vault_pass "$@"

distronode-playbook template_deepcopy/playbook.yml -i template_deepcopy/hosts "$@"
