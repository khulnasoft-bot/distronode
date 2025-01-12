#!/usr/bin/env bash

set -ux

distronode-playbook -i this,path,has,commas/hosts playbook.yml -v "$@"
