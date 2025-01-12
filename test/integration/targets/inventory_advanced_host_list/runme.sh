#!/usr/bin/env bash

set -eux

export DISTRONODE_INVENTORY_ENABLED=advanced_host_list

# A few things to make it easier to grep against adhoc
export DISTRONODE_LOAD_CALLBACK_PLUGINS=True
export DISTRONODE_STDOUT_CALLBACK=oneline

adhoc="$(distronode -i 'local[0:10],' -m ping --connection=local -e distronode_python_interpreter="{{ distronode_playbook_python }}" all -v)"

for i in $(seq 0 10); do
    grep -qE "local${i} \| SUCCESS.*\"ping\": \"pong\"" <<< "$adhoc"
done

set +e
parse_fail="$(distronode -i 'local[1:j],' -m ping --connection=local all -v 2>&1)"
set -e

grep -q "Failed to parse local\[1:j\], with advanced_host_list" <<< "$parse_fail"

# Intentionally missing comma, ensure we don't fatal.
no_comma="$(distronode -i 'local[1:5]' -m ping --connection=local all -v 2>&1)"
grep -q "No inventory was parsed" <<< "$no_comma"

# Intentionally botched range (missing end number), ensure we don't fatal.
no_end="$(distronode -i 'local[1:],' -m ping --connection=local -e distronode_python_interpreter="{{ distronode_playbook_python }}" all -vvv 2>&1)"
grep -q "Unable to parse address from hostname, leaving unchanged:" <<< "$no_end"
grep -q "host range must specify end value" <<< "$no_end"
grep -q "local\[3:\] \| SUCCESS" <<< "$no_end"

# Unset adhoc stuff
unset DISTRONODE_LOAD_CALLBACK_PLUGINS DISTRONODE_STDOUT_CALLBACK

distronode-playbook -i 'local100,local[100:110:2]' test_advanced_host_list.yml -v "$@"
