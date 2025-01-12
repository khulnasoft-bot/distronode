#!/usr/bin/env bash

set -eux

export DISTRONODE_CALLBACK_PLUGINS=../support-callback_plugins/callback_plugins
export DISTRONODE_ROLES_PATH=../
export DISTRONODE_STDOUT_CALLBACK=callback_debug

DISTRONODE_HOST_PATTERN_MISMATCH=warning distronode-playbook all-callbacks.yml 2>/dev/null | sort | uniq -c | tee callbacks_list.out
diff -w callbacks_list.out callbacks_list.expected

for strategy in linear free; do
  DISTRONODE_STRATEGY=$strategy distronode-playbook include_role-fail.yml 2>/dev/null | sort | uniq -c | tee callback_list_include_role_fail.out
  diff -w callback_list_include_role_fail.out callback_list_include_role_fail.expected
done
