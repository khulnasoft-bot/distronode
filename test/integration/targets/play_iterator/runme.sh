#!/usr/bin/env bash

set -eux

distronode-playbook playbook.yml --start-at-task 'task 2' "$@"
