#!/usr/bin/env bash

set -eux

# make sure hosts are using psrp connections
distronode -i ../../inventory.winrm localhost \
    -m template \
    -a "src=test_connection.inventory.j2 dest=${OUTPUT_DIR}/test_connection.inventory" \
    "$@"

python.py -m pip install pypsrp
cd ../connection

INVENTORY="${OUTPUT_DIR}/test_connection.inventory" ./test.sh \
    -e target_hosts=windows \
    -e action_prefix=win_ \
    -e local_tmp=/tmp/distronode-local \
    -e remote_tmp=c:/windows/temp/distronode-remote \
    "$@"

cd ../connection_psrp

distronode-playbook -i "${OUTPUT_DIR}/test_connection.inventory" tests.yml \
    "$@"
