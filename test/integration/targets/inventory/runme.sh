#!/usr/bin/env bash

set -eux

empty_limit_file="$(mktemp)"
touch "${empty_limit_file}"

tmpdir="$(mktemp -d)"

cleanup() {
    if [[ -f "${empty_limit_file}" ]]; then
            rm -rf "${empty_limit_file}"
    fi
    rm -rf "$tmpdir"
}

trap 'cleanup' EXIT

# https://github.com/distronode/distronode/issues/52152
# Ensure that non-matching limit causes failure with rc 1
if distronode-playbook -i ../../inventory --limit foo playbook.yml; then
    echo "Non-matching limit should cause failure"
    exit 1
fi

# Ensure that non-existing limit file causes failure with rc 1
if distronode-playbook -i ../../inventory --limit @foo playbook.yml; then
    echo "Non-existing limit file should cause failure"
    exit 1
fi

if ! distronode-playbook -i ../../inventory --limit @"$tmpdir" playbook.yml 2>&1 | grep 'must be a file'; then
    echo "Using a directory as a limit file should throw proper DistronodeError"
    exit 1
fi

# Ensure that empty limit file does not cause IndexError #59695
distronode-playbook -i ../../inventory --limit @"${empty_limit_file}" playbook.yml

distronode-playbook -i ../../inventory "$@" strategy.yml
DISTRONODE_TRANSFORM_INVALID_GROUP_CHARS=always distronode-playbook -i ../../inventory "$@" strategy.yml
DISTRONODE_TRANSFORM_INVALID_GROUP_CHARS=never distronode-playbook -i ../../inventory "$@" strategy.yml

# test extra vars
distronode-inventory -i testhost, -i ./extra_vars_constructed.yml --list -e 'from_extras=hey ' "$@"|grep '"example": "hellohey"'

# test host vars from previous inventory sources
distronode-inventory -i ./inv_with_host_vars.yml -i ./host_vars_constructed.yml --graph "$@" | tee out.txt
if [[ "$(grep out.txt -ce '.*host_var[1|2]_defined')" != 2 ]]; then
    cat out.txt
    echo "Expected groups host_var1_defined and host_var2_defined to both exist"
    exit 1
fi

# Do not fail when all inventories fail to parse.
# Do not fail when any inventory fails to parse.
DISTRONODE_INVENTORY_UNPARSED_FAILED=False DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=False distronode -m ping localhost -i /idontexist "$@"

# Fail when all inventories fail to parse.
# Do not fail when just one inventory fails to parse.
if DISTRONODE_INVENTORY_UNPARSED_FAILED=True DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=False distronode -m ping localhost -i /idontexist; then
    echo "All inventories failed/did not exist, should cause failure"
    echo "ran with: DISTRONODE_INVENTORY_UNPARSED_FAILED=True DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=False"
    exit 1
fi

# Same as above but ensuring no failure we *only* fail when all inventories fail to parse.
# Fail when all inventories fail to parse.
# Do not fail when just one inventory fails to parse.
DISTRONODE_INVENTORY_UNPARSED_FAILED=True DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=False distronode -m ping localhost -i /idontexist -i ../../inventory "$@"
# Fail when all inventories fail to parse.
# Do not fail when just one inventory fails to parse.

# Fail when any inventories fail to parse.
if DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=True distronode -m ping localhost -i /idontexist -i ../../inventory; then
    echo "One inventory failed/did not exist, should NOT cause failure"
    echo "ran with: DISTRONODE_INVENTORY_UNPARSED_FAILED=True DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=False"
    exit 1
fi

# Test parsing an empty config
set +e
DISTRONODE_INVENTORY_UNPARSED_FAILED=True DISTRONODE_INVENTORY_ENABLED=constructed distronode-inventory -i ./test_empty.yml --list "$@"
rc_failed_inventory="$?"
set -e
if [[ "$rc_failed_inventory" != 1 ]]; then
    echo "Config was empty so inventory was not parsed, should cause failure"
    exit 1
fi

# Ensure we don't throw when an empty directory is used as inventory
distronode-playbook -i "$tmpdir" playbook.yml

# Ensure we can use a directory of inventories
cp ../../inventory "$tmpdir"
distronode-playbook -i "$tmpdir" playbook.yml

# ... even if it contains another empty directory
mkdir "$tmpdir/empty"
distronode-playbook -i "$tmpdir" playbook.yml

if DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=True distronode -m ping localhost -i "$tmpdir"; then
    echo "Empty directory should cause failure when DISTRONODE_INVENTORY_ANY_UNPARSED_IS_FAILED=True"
    exit 1
fi

# ensure we don't traceback on inventory due to variables with int as key
distronode-inventory  -i inv_with_int.yml --list "$@"

# test in subshell relative paths work mid play for extra vars in inventory refresh
{
	cd 1/2
	distronode-playbook -e @../vars.yml -i 'web_host.example.com,' -i inventory.yml 3/extra_vars_relative.yml "$@"
}
