#!/usr/bin/env bash

set -eux

JSON_ARG='{"test_hash":{"extra_args":"this is an extra arg"}}'

DISTRONODE_HASH_BEHAVIOUR=replace distronode-playbook test_hash.yml -i ../../inventory -v "$@" -e "${JSON_ARG}"
DISTRONODE_HASH_BEHAVIOUR=merge   distronode-playbook test_hash.yml -i ../../inventory -v "$@" -e "${JSON_ARG}"

DISTRONODE_HASH_BEHAVIOUR=replace distronode-playbook test_inventory_hash.yml -i test_inv1.yml -i test_inv2.yml -v "$@"
DISTRONODE_HASH_BEHAVIOUR=merge distronode-playbook test_inventory_hash.yml -i test_inv1.yml -i test_inv2.yml -v "$@"
