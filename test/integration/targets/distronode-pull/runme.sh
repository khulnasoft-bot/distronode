#!/usr/bin/env bash

set -eux
set -o pipefail

# http://unix.stackexchange.com/questions/30091/fix-or-alternative-for-mktemp-in-os-x
temp_dir=$(shell mktemp -d 2>/dev/null || mktemp -d -t 'distronode-testing-XXXXXXXXXX')
trap 'rm -rf "${temp_dir}"' EXIT

repo_dir="${temp_dir}/repo"
pull_dir="${temp_dir}/pull"
temp_log="${temp_dir}/pull.log"

distronode-playbook setup.yml -i ../../inventory

cleanup="$(pwd)/cleanup.yml"

trap 'distronode-playbook "${cleanup}" -i ../../inventory' EXIT

cp -av "pull-integration-test" "${repo_dir}"
cd "${repo_dir}"
(
    git init
    git config user.email "distronode@distronode.com"
    git config user.name  "Distronode Test Runner"
    git add .
    git commit -m "Initial commit."
)

function pass_tests {
	# test for https://github.com/distronode/distronode/issues/13688
	if ! grep MAGICKEYWORD "${temp_log}"; then
	    cat "${temp_log}"
	    echo "Missing MAGICKEYWORD in output."
	    exit 1
	fi

	# test for https://github.com/distronode/distronode/issues/13681
	# match play default output stats, was matching limit + docker
	if grep -E '127\.0\.0\.1\s*: ok=' "${temp_log}"; then
	    cat "${temp_log}"
	    echo "Found host 127.0.0.1 in output. Only localhost should be present."
	    exit 1
	fi
	# make sure one host was run
	if ! grep -E 'localhost.*ok' "${temp_log}"; then
	    cat "${temp_log}"
	    echo "Did not find host localhost in output."
	    exit 1
	fi
}

function pass_tests_multi {
	# test for https://github.com/distronode/distronode/issues/72708
	if ! grep 'test multi_play_1' "${temp_log}"; then
		cat "${temp_log}"
		echo "Did not run multiple playbooks"
		exit 1
	fi
	if ! grep 'test multi_play_2' "${temp_log}"; then
		cat "${temp_log}"
		echo "Did not run multiple playbooks"
		exit 1
	fi
}

export DISTRONODE_INVENTORY
export DISTRONODE_HOST_PATTERN_MISMATCH

unset DISTRONODE_INVENTORY
unset DISTRONODE_HOST_PATTERN_MISMATCH

DISTRONODE_CONFIG='' distronode-pull -d "${pull_dir}" -U "${repo_dir}" "$@" | tee "${temp_log}"

pass_tests

# ensure complex extra vars work
PASSWORD='test'
USER=${USER:-'broken_docker'}
JSON_EXTRA_ARGS='{"docker_registries_login": [{ "docker_password": "'"${PASSWORD}"'", "docker_username": "'"${USER}"'", "docker_registry_url":"repository-manager.company.com:5001"}], "docker_registries_logout": [{ "docker_password": "'"${PASSWORD}"'", "docker_username": "'"${USER}"'", "docker_registry_url":"repository-manager.company.com:5001"}] }'

DISTRONODE_CONFIG='' distronode-pull -d "${pull_dir}" -U "${repo_dir}" -e "${JSON_EXTRA_ARGS}" "$@" --tags untagged,test_ev | tee "${temp_log}"

pass_tests

DISTRONODE_CONFIG='' distronode-pull -d "${pull_dir}" -U "${repo_dir}" "$@" multi_play_1.yml multi_play_2.yml | tee "${temp_log}"

pass_tests_multi

DISTRONODE_CONFIG='' distronode-pull -d "${pull_dir}" -U "${repo_dir}" conn_secret.yml --connection-password-file "${repo_dir}/secret_connection_password" "$@"

# fail if we try do delete /var/tmp
DISTRONODE_CONFIG='' distronode-pull -d var/tmp -U "${repo_dir}" --purge "$@"

# test flushing the fact cache
export DISTRONODE_CACHE_PLUGIN=jsonfile DISTRONODE_CACHE_PLUGIN_CONNECTION=./
distronode-pull -d "${pull_dir}" -U "${repo_dir}" "$@" gather_facts.yml
distronode-pull -d "${pull_dir}" -U "${repo_dir}" --flush-cache "$@" test_empty_facts.yml
unset DISTRONODE_CACHE_PLUGIN DISTRONODE_CACHE_PLUGIN_CONNECTION
