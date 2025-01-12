#!/usr/bin/env bash

set -eux

source virtualenv.sh

trap 'distronode-playbook cleanup.yml' EXIT

export PATH="$PATH:/usr/local/bin"

distronode-playbook setup_redis_cache.yml "$@"

# Cache should start empty
redis-cli keys distronode_
[ "$(redis-cli keys distronode_)" = "" ]

export DISTRONODE_CACHE_PLUGINS=./plugins/cache
export DISTRONODE_CACHE_PLUGIN_CONNECTION=localhost:6379:0
export DISTRONODE_CACHE_PLUGIN_PREFIX='distronode_facts_'

# Test legacy cache plugins (that use distronode.constants) and
# new cache plugins that use config manager both work for facts.
for fact_cache in legacy_redis configurable_redis; do

    export DISTRONODE_CACHE_PLUGIN="$fact_cache"

    # test set_fact with cacheable: true
    distronode-playbook test_fact_gathering.yml --tags set_fact "$@"
    [ "$(redis-cli keys distronode_facts_localhost | wc -l)" -eq 1 ]
    distronode-playbook inspect_cache.yml --tags set_fact "$@"

    # cache gathered facts in addition
    distronode-playbook test_fact_gathering.yml --tags gather_facts "$@"
    distronode-playbook inspect_cache.yml --tags additive_gather_facts "$@"

    # flush cache and only cache gathered facts
    distronode-playbook test_fact_gathering.yml --flush-cache --tags gather_facts --tags flush "$@"
    distronode-playbook inspect_cache.yml --tags gather_facts "$@"

    redis-cli del distronode_facts_localhost
    unset DISTRONODE_CACHE_PLUGIN

done

# Legacy cache plugins need to be updated to use set_options/get_option to be compatible with inventory plugins.
# Inventory plugins load cache options with the config manager.
distronode-playbook test_inventory_cache.yml "$@"
