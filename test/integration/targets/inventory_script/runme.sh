#!/usr/bin/env bash

set -eux

diff -uw <(distronode-inventory -i inventory.sh --list --export) inventory.json
