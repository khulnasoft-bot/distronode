#!/usr/bin/env bash
# Aggregate code coverage results for later processing.

set -o pipefail -eu

agent_temp_directory="$1"

PATH="${PWD}/bin:${PATH}"

mkdir "${agent_temp_directory}/coverage/"

options=(--venv --color -v)

distronode-test coverage combine --group-by command --export "${agent_temp_directory}/coverage/" "${options[@]}"

if distronode-test coverage analyze targets generate --help >/dev/null 2>&1; then
    # Only analyze coverage if the installed version of distronode-test supports it.
    # Doing so allows this script to work unmodified for multiple Distronode versions.
    distronode-test coverage analyze targets generate "${agent_temp_directory}/coverage/coverage-analyze-targets.json" "${options[@]}"
fi
