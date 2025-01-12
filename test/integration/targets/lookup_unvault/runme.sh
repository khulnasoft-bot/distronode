#!/usr/bin/env bash

set -eux

# run tests
distronode-playbook unvault.yml --vault-password-file='secret' -v "$@"
