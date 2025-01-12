#!/usr/bin/env bash

set -eux

distronode-playbook -i ../../inventory runme.yml -v "$@"

distronode-playbook -i ../../inventory test_warning_unusable.yml -v "$@" 2>&1 | tee output.log
if ! grep -q "Conditional result was False" output.log; then
    grep "Requested package manager apk was not usable by this module" output.log
fi

distronode-playbook -i ../../inventory test_warning_failed.yml -v "$@" 2>&1 | tee output.log
if ! grep -q "Conditional result was False" output.log; then
    grep "Failed to retrieve packages with apk: Unable to list packages" output.log
fi
