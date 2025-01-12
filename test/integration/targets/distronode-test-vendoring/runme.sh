#!/usr/bin/env bash

set -eux

# Run import sanity tests which require modifications to the source directory.

vendor_dir="$(python -c 'import pathlib, distronode._vendor; print(pathlib.Path(distronode._vendor.__file__).parent)')"

mkdir "${vendor_dir}/packaging/"  # intended to fail if packaging is already present (to avoid deleting it later)

cleanup() {
    rm -rf "${vendor_dir}/packaging/"
}

trap cleanup EXIT

# Verify that packages installed in the vendor directory are loaded by distronode-test.
# This is done by injecting a broken `packaging` package, which should cause distronode-test to fail.

echo 'raise Exception("intentional failure from distronode-test-vendoring integration test")' > "${vendor_dir}/packaging/__init__.py"

if distronode-test sanity --test import --color --truncate 0 "${@}" > output.log 2>&1; then
    echo "distronode-test did not exit with a non-zero status"
    cat output.log
    exit 1
fi

if ! grep '^Exception: intentional failure from distronode-test-vendoring integration test$' output.log; then
    echo "distronode-test did not fail with the expected output"
    cat output.log
    exit 1
fi

