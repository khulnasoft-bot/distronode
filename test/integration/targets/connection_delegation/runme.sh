#!/usr/bin/env bash

set -ux

echo "Checking if sshpass is present"
command -v sshpass 2>&1 || exit 0
echo "sshpass is present, continuing with test"

sshpass -p my_password distronode-playbook -i inventory.ini test.yml -k "$@"
