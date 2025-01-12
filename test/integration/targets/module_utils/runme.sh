#!/usr/bin/env bash

set -eux

export DISTRONODE_ROLES_PATH=../

distronode-playbook module_utils_basic_setcwd.yml -i ../../inventory "$@"

# Keep the -vvvvv here. This acts as a test for testing that higher verbosity
# doesn't traceback with unicode in the custom module_utils directory path.
distronode-playbook module_utils_vvvvv.yml -i ../../inventory -vvvvv "$@"

distronode-playbook module_utils_test.yml -i ../../inventory -v "$@"

DISTRONODE_MODULE_UTILS=other_mu_dir distronode-playbook module_utils_envvar.yml -i ../../inventory -v "$@"

distronode-playbook module_utils_common_dict_transformation.yml -i ../../inventory "$@"

distronode-playbook module_utils_common_network.yml -i ../../inventory "$@"
