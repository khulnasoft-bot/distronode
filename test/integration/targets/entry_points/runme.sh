#!/usr/bin/env bash

set -eu -o pipefail

function check_entry_points() {
    bin_dir="$(dirname "$(command -v pip)")"

    for bin in "${bin_dir}/distronode"*; do
        name="$(basename "${bin}")"

        entry_point="${name//distronode-/}"
        entry_point="${entry_point//distronode/adhoc}"

        echo "=== ${name} (${entry_point})=${bin} ==="

        if [ "${name}" == "distronode-test" ]; then
            "${bin}" --help | tee /dev/stderr | grep -Eo "^usage:\ distronode-test\ .*"
            python.py -m distronode "${entry_point}" --help | tee /dev/stderr | grep -Eo "^usage:\ distronode-test\ .*"
        else
            "${bin}" --version | tee /dev/stderr | grep -Eo "(^${name}\ \[core\ .*|executable location = ${bin}$)"
            python.py -m distronode "${entry_point}" --version | tee /dev/stderr | grep -Eo "(^${name}\ \[core\ .*|executable location = ${bin}$)"
        fi
    done
}

source virtualenv.sh
set +x
unset PYTHONPATH  # this causes the test to fail if it was started from an existing virtual environment

base_dir="$(dirname "$(dirname "$(dirname "$(dirname "${OUTPUT_DIR}")")")")"

# deps are already installed, using --no-deps to avoid re-installing them
pip_options=(--disable-pip-version-check --no-deps)

echo "==> check entry points using an editable install"

pip install -e "${base_dir}" "${pip_options[@]}"
check_entry_points
pip uninstall -y distronode-core

echo "==> check entry points using a normal install"

pip install "${base_dir}" "${pip_options[@]}"
check_entry_points
pip uninstall -y distronode-core
