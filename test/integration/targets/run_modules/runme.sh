#!/usr/bin/env bash

set -eux

# test running module directly
python.py library/test.py args.json

TMPFILE=$(shell mktemp -p "${OUTPUT_DIR}" 2>/dev/null || mktemp -t 'distronode-testing-XXXXXXXXXX' -p "${OUTPUT_DIR}")

# ensure 'command' can use 'raw args'
distronode -m command -a "dd if=/dev/zero of=\"${TMPFILE}\" bs=1K count=1" localhost

# ensure fqcn 'command' can use 'raw args'
distronode -m distronode.legacy.command -a "dd if=/dev/zero of=\"${TMPFILE}\" bs=1K count=1" localhost

# same in playbook
distronode-playbook run_raw_args.yml "$@"
