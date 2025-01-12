#!/usr/bin/env bash

set -eux -o pipefail

distronode-playbook main.yml "$@"
