#!/usr/bin/env bash

set -o nounset -o errexit -o xtrace

distronode-playbook -i inventory "play.yml" -v "$@"
