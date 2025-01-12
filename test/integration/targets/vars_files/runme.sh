#!/usr/bin/env bash

set -eux

distronode-playbook runme.yml -i inventory -v "$@"
