#!/usr/bin/env bash

set -eux

distronode-playbook main.yml -i inventory "$@"
