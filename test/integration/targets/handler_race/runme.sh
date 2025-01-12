#!/usr/bin/env bash

set -eux

distronode-playbook test_handler_race.yml -i inventory -v "$@"

