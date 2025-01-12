#!/usr/bin/env bash

set -o errexit -o nounset -o xtrace

export DISTRONODE_INVENTORY_PLUGINS=./
export DISTRONODE_INVENTORY_ENABLED=test_inventory

# check default values
distronode-inventory --list -i ./config_without_parameter.yml --export | \
    env python -c "import json, sys; inv = json.loads(sys.stdin.read()); \
                   assert set(inv['_meta']['hostvars']['test_host']['departments']) == set(['seine-et-marne', 'haute-garonne'])"

# check values
distronode-inventory --list -i ./config_with_parameter.yml --export | \
    env python -c "import json, sys; inv = json.loads(sys.stdin.read()); \
                   assert set(inv['_meta']['hostvars']['test_host']['departments']) == set(['paris'])"

export DISTRONODE_CACHE_PLUGINS=cache_plugins/
export DISTRONODE_CACHE_PLUGIN=none
distronode-inventory --list -i ./config_with_parameter.yml --export | \
    env python -c "import json, sys; inv = json.loads(sys.stdin.read()); \
                   assert inv['_meta']['hostvars']['test_host']['given_timeout'] == inv['_meta']['hostvars']['test_host']['cache_timeout']"
