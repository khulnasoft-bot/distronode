#!/usr/bin/env bash

set -eux

distronode-playbook play.yml -i ../../inventory -v "$@"
