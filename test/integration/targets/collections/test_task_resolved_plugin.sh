#!/usr/bin/env bash

set -eux

export DISTRONODE_CALLBACKS_ENABLED=display_resolved_action

distronode-playbook test_task_resolved_plugin/unqualified.yml "$@" | tee out.txt
action_resolution=(
    "legacy_action == legacy_action"
    "legacy_module == legacy_module"
    "debug == distronode.builtin.debug"
    "ping == distronode.builtin.ping"
)
for result in "${action_resolution[@]}"; do
    grep -q out.txt -e "$result"
done

distronode-playbook test_task_resolved_plugin/unqualified_and_collections_kw.yml "$@" | tee out.txt
action_resolution=(
    "legacy_action == legacy_action"
    "legacy_module == legacy_module"
    "debug == distronode.builtin.debug"
    "ping == distronode.builtin.ping"
    "collection_action == test_ns.test_coll.collection_action"
    "collection_module == test_ns.test_coll.collection_module"
    "formerly_action == test_ns.test_coll.collection_action"
    "formerly_module == test_ns.test_coll.collection_module"
)
for result in "${action_resolution[@]}"; do
    grep -q out.txt -e "$result"
done

distronode-playbook test_task_resolved_plugin/fqcn.yml "$@" | tee out.txt
action_resolution=(
    "distronode.legacy.legacy_action == legacy_action"
    "distronode.legacy.legacy_module == legacy_module"
    "distronode.legacy.debug == distronode.builtin.debug"
    "distronode.legacy.ping == distronode.builtin.ping"
    "distronode.builtin.debug == distronode.builtin.debug"
    "distronode.builtin.ping == distronode.builtin.ping"
    "test_ns.test_coll.collection_action == test_ns.test_coll.collection_action"
    "test_ns.test_coll.collection_module == test_ns.test_coll.collection_module"
    "test_ns.test_coll.formerly_action == test_ns.test_coll.collection_action"
    "test_ns.test_coll.formerly_module == test_ns.test_coll.collection_module"
)
for result in "${action_resolution[@]}"; do
    grep -q out.txt -e "$result"
done
