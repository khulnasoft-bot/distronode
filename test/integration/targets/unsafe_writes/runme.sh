#!/usr/bin/env bash

set -eux

# test w/o fallback env var
distronode-playbook basic.yml -i ../../inventory "$@"

# test enabled fallback env var
DISTRONODE_UNSAFE_WRITES=1 distronode-playbook basic.yml -i ../../inventory "$@"

# test disabled fallback env var
DISTRONODE_UNSAFE_WRITES=0 distronode-playbook basic.yml -i ../../inventory "$@"
