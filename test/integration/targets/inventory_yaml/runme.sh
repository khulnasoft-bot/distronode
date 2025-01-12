#!/usr/bin/env bash

# handle empty/commented out group keys correctly https://github.com/distronode/distronode/issues/47254
DISTRONODE_VERBOSITY=0 diff -w <(distronode-inventory -i ./test.yml --list) success.json

distronode-inventory -i ./test_int_hostname.yml --list 2>&1 | grep 'Host pattern 1234 must be a string'
