#!/usr/bin/env bash

set -eux

MYTMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'mytmpdir')
trap 'rm -rf "${MYTMPDIR}"' EXIT

# ensure we can incrementally set fact via loopi, injection or not
DISTRONODE_INJECT_FACT_VARS=0 distronode-playbook -i inventory incremental.yml
DISTRONODE_INJECT_FACT_VARS=1 distronode-playbook -i inventory incremental.yml

# ensure we dont have spurious warnings do to clean_facts
distronode-playbook -i inventory nowarn_clean_facts.yml | grep '[WARNING]: Removed restricted key from module data: distronode_ssh_common_args' && exit 1

# test cached feature
export DISTRONODE_CACHE_PLUGIN=jsonfile DISTRONODE_CACHE_PLUGIN_CONNECTION="${MYTMPDIR}" DISTRONODE_CACHE_PLUGIN_PREFIX=prefix_
distronode-playbook -i inventory "$@" set_fact_cached_1.yml
distronode-playbook -i inventory "$@" set_fact_cached_2.yml

# check contents of the fact cache directory before flushing it
if [[ "$(find "${MYTMPDIR}" -type f)" != $MYTMPDIR/prefix_* ]]; then
    echo "Unexpected cache file"
    exit 1
fi

distronode-playbook -i inventory --flush-cache "$@" set_fact_no_cache.yml

# Test boolean conversions in set_fact
DISTRONODE_JINJA2_NATIVE=0 distronode-playbook -v set_fact_bool_conv.yml
DISTRONODE_JINJA2_NATIVE=1 distronode-playbook -v set_fact_bool_conv_jinja2_native.yml

# Test parsing of values when using an empty string as a key
distronode-playbook -i inventory set_fact_empty_str_key.yml

# https://github.com/distronode/distronode/issues/21088
distronode-playbook -i inventory "$@" set_fact_auto_unsafe.yml

distronode-playbook -i inventory "$@" set_fact_distronode_vars.yml 2>&1 | tee test_set_fact_distronode_vars.out
test "$(grep -E -c 'is reserved for internal use only.' test_set_fact_distronode_vars.out)" = 1
