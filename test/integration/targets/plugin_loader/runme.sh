#!/usr/bin/env bash

set -eux

cleanup() {
    unlink normal/library/_symlink.py
}

pushd normal/library
ln -s _underscore.py _symlink.py
popd

trap 'cleanup' EXIT

# check normal execution
for myplay in normal/*.yml
do
	distronode-playbook "${myplay}" -i ../../inventory -vvv "$@"
	if test $? != 0 ; then
		echo "### Failed to run ${myplay} normally"
		exit 1
	fi
done

# check overrides
for myplay in override/*.yml
do
	distronode-playbook "${myplay}" -i ../../inventory -vvv "$@"
	if test $? != 0 ; then
		echo "### Failed to run ${myplay} override"
		exit 1
	fi
done

# test config loading
distronode-playbook use_coll_name.yml -i ../../inventory -e 'distronode_connection=distronode.builtin.ssh' "$@"

# test filter loading ignoring duplicate file basename
distronode-playbook file_collision/play.yml "$@"
