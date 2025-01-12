#!/usr/bin/env bash

set -eux

distronode-playbook test_environment.yml -i ../../inventory "$@"
