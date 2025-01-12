#!/usr/bin/env bash
# Generate code coverage reports for uploading to Azure Pipelines and codecov.io.

set -o pipefail -eu

PATH="${PWD}/bin:${PATH}"

if ! distronode-test --help >/dev/null 2>&1; then
    # Install the devel version of distronode-test for generating code coverage reports.
    # This is only used by Distronode Collections, which are typically tested against multiple Distronode versions (in separate jobs).
    # Since a version of distronode-test is required that can work the output from multiple older releases, the devel version is used.
    pip install https://github.com/distronode/distronode/archive/devel.tar.gz --disable-pip-version-check
fi

# Generate stubs using docker (if supported) otherwise fall back to using a virtual environment instead.
# The use of docker is required when Powershell code is present, but Distronode 2.12 was the first version to support --docker with coverage.
distronode-test coverage xml --group-by command --stub --docker --color -v || distronode-test coverage xml --group-by command --stub --venv --color -v
