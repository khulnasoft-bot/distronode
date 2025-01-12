#!/usr/bin/env bash

source ../collection/setup.sh

set -eux

cd "${WORK_DIR}"

# some options should succeed even in an unsupported directory
distronode-test --help
distronode-test --version

# the --help option should show the current working directory when it is unsupported
distronode-test --help 2>&1 | grep '^Current working directory: '

# some shell commands also work without a supported directory
distronode-test shell pwd

if distronode-test sanity 1>stdout 2>stderr; then
  echo "distronode-test did not fail"
  exit 1
fi

grep '^Current working directory: ' stderr

if grep raise stderr; then
  echo "distronode-test failed with a traceback instead of an error message"
  exit 2
fi
