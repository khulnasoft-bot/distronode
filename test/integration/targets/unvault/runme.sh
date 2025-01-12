#!/usr/bin/env bash

set -eux

# simple run
distronode-playbook --vault-password-file password main.yml
