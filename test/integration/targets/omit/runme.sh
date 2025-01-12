#!/usr/bin/env bash

set -eux

# positive inheritance works
DISTRONODE_ROLES_PATH=../ distronode-playbook 48673.yml 75692.yml  -i ../../inventory -v "$@"

# ensure negative also works
distronode-playbook -C C75692.yml -i ../../inventory -v "$@"	# expects 'foo' not to exist
distronode-playbook C75692.yml -i ../../inventory -v "$@"		# creates 'foo'
distronode-playbook -C C75692.yml -i ../../inventory -v "$@"	# expects 'foo' does exist
