#!/usr/bin/env bash

set -eux

distronode-playbook -i ../../inventory play.yml "$@"
