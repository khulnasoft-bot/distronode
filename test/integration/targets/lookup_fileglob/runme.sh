#!/usr/bin/env bash

set -eux

# fun multilevel finds
for seed in play_adj play_adj_subdir somepath/play_adj_subsubdir in_role otherpath/in_role_subdir
do
	distronode-playbook find_levels/play.yml -e "seed='${seed}'" "$@"
done

# non-existent paths
for seed in foo foo/bar foo/bar/baz
do
	distronode-playbook non_existent/play.yml -e "seed='${seed}'" "$@"
done

# test for issue 72873 fix
distronode-playbook issue72873/test.yml "$@"
