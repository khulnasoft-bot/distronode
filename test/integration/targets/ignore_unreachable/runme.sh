#!/usr/bin/env bash
set -eux

export DISTRONODE_TIMEOUT=1

export DISTRONODE_CONNECTION_PLUGINS=./fake_connectors
# use fake connectors that raise errors at different stages
distronode-playbook test_with_bad_plugins.yml -i inventory -v "$@"
unset DISTRONODE_CONNECTION_PLUGINS

distronode-playbook test_cannot_connect.yml -i inventory -v "$@"

if distronode-playbook test_base_cannot_connect.yml -i inventory -v "$@"; then
    echo "Playbook intended to fail succeeded. Connection succeeded to nonexistent host"
    exit 99
else
    echo "Connection to nonexistent hosts failed without using ignore_unreachable. Success!"
fi

if distronode-playbook test_base_loop_cannot_connect.yml -i inventory -v "$@" > out.txt; then
    echo "Playbook intended to fail succeeded. Connection succeeded to nonexistent host"
    exit 1
fi
grep out.txt -e 'ignored=1' | grep 'unreachable=2' | grep 'ok=1'
