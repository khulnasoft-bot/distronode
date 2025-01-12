#!/usr/bin/env bash
# This test ensures that the bin entry points created by distronode-test work
# when distronode-test is running from an install instead of from source.

set -eux

# The third PATH entry is the injected bin directory created by distronode-test.
bin_dir="$(python -c 'import os; print(os.environ["PATH"].split(":")[2])')"

while IFS= read -r name
do
    bin="${bin_dir}/${name}"

    entry_point="${name//distronode-/}"
    entry_point="${entry_point//distronode/adhoc}"

    echo "=== ${name} (${entry_point})=${bin} ==="

    if [ "${name}" == "distronode-test" ]; then
        echo "skipped - distronode-test does not support self-testing from an install"
    else
        "${bin}" --version | tee /dev/stderr | grep -Eo "(^${name}\ \[core\ .*|executable location = ${bin}$)"
    fi
done < entry-points.txt
