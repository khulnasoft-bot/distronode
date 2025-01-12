#!/usr/bin/env bash

set -eux

distronode-playbook delegate_facts.yml -i inventory "$@"
