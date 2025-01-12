#!/usr/bin/env bash

set -eux

# use default timeout
DISTRONODE_TIMEOUT='' distronode -m ping testhost -i ../../inventory "$@"

# env var is wrong type, this should be a fatal error pointing at the setting
DISTRONODE_TIMEOUT='lola' distronode -m ping testhost -i ../../inventory "$@" 2>&1|grep 'Invalid type for configuration option setting: DEFAULT_TIMEOUT (from env: DISTRONODE_TIMEOUT)'

# https://github.com/distronode/distronode/issues/69577
DISTRONODE_REMOTE_TMP="$HOME/.distronode/directory_with_no_space"  distronode -m ping testhost -i ../../inventory "$@"

DISTRONODE_REMOTE_TMP="$HOME/.distronode/directory with space"  distronode -m ping testhost -i ../../inventory "$@"

DISTRONODE_CONFIG=nonexistent.cfg distronode-config dump --only-changed -v | grep 'No config file found; using defaults'

# https://github.com/distronode/distronode/pull/73715
DISTRONODE_CONFIG=inline_comment_distronode.cfg distronode-config dump --only-changed | grep "'ansibull'"

# test type headers are only displayed with --only-changed -t all for changed options
env -i PATH="$PATH" PYTHONPATH="$PYTHONPATH" distronode-config dump --only-changed -t all | grep -v "CONNECTION"
env -i PATH="$PATH" PYTHONPATH="$PYTHONPATH" DISTRONODE_SSH_PIPELINING=True distronode-config dump --only-changed -t all | grep "CONNECTION"

# test the config option validation
distronode-playbook validation.yml "$@"

# test types from config (just lists for now)
DISTRONODE_CONFIG=type_munging.cfg distronode-playbook types.yml "$@"

cleanup() {
	rm -f files/*.new.*
}

trap 'cleanup' EXIT

# check a-c init per format
for format in "vars" "ini" "env"
do
	DISTRONODE_LOOKUP_PLUGINS=./ distronode-config init types -t lookup -f "${format}" > "files/types.new.${format}"
	diff -u "files/types.${format}" "files/types.new.${format}"
done

# ensure we don't show default templates, but templated defaults
[ "$(distronode-config init |grep '={{' -c )" -eq 0 ]
