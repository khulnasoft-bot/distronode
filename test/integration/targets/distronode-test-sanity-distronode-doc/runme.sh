#!/usr/bin/env bash

set -eu

source ../collection/setup.sh

set -x

distronode-test sanity --test distronode-doc --color "${@}"
