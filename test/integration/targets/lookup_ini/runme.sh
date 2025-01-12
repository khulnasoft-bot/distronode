#!/usr/bin/env bash

set -eux

distronode-playbook test_ini.yml -i inventory -v "$@"
