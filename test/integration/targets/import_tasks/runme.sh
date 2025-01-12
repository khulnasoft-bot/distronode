#!/usr/bin/env bash

set -eux

distronode-playbook inherit_notify.yml "$@"
