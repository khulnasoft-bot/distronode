#!/usr/bin/env bash

set -eux

distronode-playbook traceback.yml -i inventory "$@"
