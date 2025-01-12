#!/usr/bin/env bash

set -eux

trap 'rm -f out' EXIT

distronode-playbook main.yml -i ../../inventory | tee out
for i in 1 2 3; do
  grep "ok: \[localhost\] => (item=$i)" out
  grep "\"item\": $i" out
done

distronode-playbook main_fqcn.yml -i ../../inventory | tee out
for i in 1 2 3; do
  grep "ok: \[localhost\] => (item=$i)" out
  grep "\"item\": $i" out
done

# ensure debug does not set top level vars when looking at distronode_facts
distronode-playbook nosetfacts.yml "$@"
