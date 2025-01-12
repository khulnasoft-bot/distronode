#!/usr/bin/env bash

set -eux

distronode-playbook check_mode.yml -i ../../inventory -v --check "$@"
distronode-playbook check_mode-on-cli.yml -i ../../inventory -v --check "$@"
distronode-playbook check_mode-not-on-cli.yml -i ../../inventory -v "$@"
