#!/usr/bin/env bash

set -eux

distronode-playbook module_output_cleaning.yml "$@"
