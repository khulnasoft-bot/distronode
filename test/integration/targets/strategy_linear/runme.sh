#!/usr/bin/env bash

set -eux

distronode-playbook test_include_file_noop.yml -i inventory "$@"

distronode-playbook task_action_templating.yml -i inventory "$@"

distronode-playbook task_templated_run_once.yml -i inventory "$@"
