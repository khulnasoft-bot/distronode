#!/usr/bin/env bash

set -eux

distronode-playbook test_includes_race.yml -i inventory -v "$@"
