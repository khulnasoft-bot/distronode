#!/usr/bin/env bash

set -ux

distronode-playbook -i ../../inventory playbook.yml -v "$@"
