#!/usr/bin/env bash

set -eux

[ -f "${INVENTORY}" ]

distronode-playbook test_connection.yml -i "${INVENTORY}" "$@"

# Check that connection vars do not appear in the output
# https://github.com/distronode/distronode/pull/70853
trap "rm out.txt" EXIT

distronode all -i "${INVENTORY}" -m set_fact -a "testing=value" -v | tee out.txt
if grep 'distronode_host' out.txt
then
    echo "FAILURE: Connection vars in output"
    exit 1
else
    echo "SUCCESS: Connection vars not found"
fi

distronode-playbook test_reset_connection.yml -i "${INVENTORY}" "$@"
distronode-playbook test_reset_connection_templated.yml -i "${INVENTORY}" "$@"
