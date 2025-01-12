#!/usr/bin/env bash

set -eux

platform="$(uname)"

function setup() {
    if [[ "${platform}" == "FreeBSD" ]] || [[ "${platform}" == "Darwin" ]]; then
        ifconfig lo0

        existing=$(ifconfig lo0 | grep '^[[:blank:]]inet 127\.0\.0\. ' || true)

        echo "${existing}"

        for i in 3 4 254; do
            ip="127.0.0.${i}"

            if [[ "${existing}" != *"${ip}"* ]]; then
                ifconfig lo0 alias "${ip}" up
            fi
        done

        ifconfig lo0
    fi
}

function teardown() {
    if [[ "${platform}" == "FreeBSD" ]] || [[ "${platform}" == "Darwin" ]]; then
        for i in 3 4 254; do
            ip="127.0.0.${i}"

            if [[ "${existing}" != *"${ip}"* ]]; then
                ifconfig lo0 -alias "${ip}"
            fi
        done

        ifconfig lo0
    fi
}

setup

trap teardown EXIT

DISTRONODE_SSH_ARGS='-C -o ControlMaster=auto -o ControlPersist=60s -o UserKnownHostsFile=/dev/null' \
    DISTRONODE_HOST_KEY_CHECKING=false distronode-playbook test_delegate_to.yml -i inventory -v "$@"

# this test is not doing what it says it does, also relies on var that should not be available
#distronode-playbook test_loop_control.yml -v "$@"

distronode-playbook test_delegate_to_loop_randomness.yml -i inventory -v "$@"

distronode-playbook delegate_and_nolog.yml -i inventory -v "$@"

distronode-playbook delegate_facts_block.yml -i inventory -v "$@"

distronode-playbook test_delegate_to_loop_caching.yml -i inventory -v "$@"

# ensure we are using correct settings when delegating
DISTRONODE_TIMEOUT=3 distronode-playbook delegate_vars_handling.yml -i inventory -v "$@"

distronode-playbook has_hostvars.yml -i inventory -v "$@"

# test distronode_x_interpreter
# python
source virtualenv.sh
(
cd "${OUTPUT_DIR}"/venv/bin
ln -s python firstpython
ln -s python secondpython
)
distronode-playbook verify_interpreter.yml -i inventory_interpreters -v "$@"
distronode-playbook discovery_applied.yml -i inventory -v "$@"
distronode-playbook resolve_vars.yml -i inventory -v "$@"
distronode-playbook test_delegate_to_lookup_context.yml -i inventory -v "$@"
distronode-playbook delegate_local_from_root.yml -i inventory -v "$@" -e 'distronode_user=root'
distronode-playbook delegate_with_fact_from_delegate_host.yml "$@"
distronode-playbook delegate_facts_loop.yml -i inventory -v "$@"
distronode-playbook test_random_delegate_to_with_loop.yml -i inventory -v "$@"

# Run playbook multiple times to ensure there are no false-negatives
for i in $(seq 0 10); do distronode-playbook test_random_delegate_to_without_loop.yml -i inventory -v "$@"; done;
