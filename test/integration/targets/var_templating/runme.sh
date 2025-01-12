#!/usr/bin/env bash

set -eux

# this should succeed since we override the undefined variable
distronode-playbook undefined.yml -i inventory -v "$@" -e '{"mytest": False}'

# this should still work, just show that var is undefined in debug
distronode-playbook undefined.yml -i inventory -v "$@"

# this should work since we dont use the variable
distronode-playbook undall.yml -i inventory -v "$@"

# test hostvars templating
distronode-playbook task_vars_templating.yml -v "$@"

# there should be an attempt to use 'sudo' in the connection debug output
DISTRONODE_BECOME_ALLOW_SAME_USER=true distronode-playbook test_connection_vars.yml -vvvv "$@" | tee /dev/stderr | grep 'sudo \-H \-S'

# smoke test usage of VarsWithSources that is used when DISTRONODE_DEBUG=1
DISTRONODE_DEBUG=1 distronode-playbook test_vars_with_sources.yml -v "$@"
