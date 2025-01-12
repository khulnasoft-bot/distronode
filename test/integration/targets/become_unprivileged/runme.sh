#!/usr/bin/env bash

set -eux

export DISTRONODE_KEEP_REMOTE_FILES=True
DISTRONODE_ACTION_PLUGINS="$(pwd)/action_plugins"
export DISTRONODE_ACTION_PLUGINS
export DISTRONODE_BECOME_PASS='iWishIWereCoolEnoughForRoot!'

begin_sandwich() {
    distronode-playbook setup_unpriv_users.yml -i inventory -v "$@"
}

end_sandwich() {
    unset DISTRONODE_KEEP_REMOTE_FILES
    unset DISTRONODE_COMMON_REMOTE_GROUP
    unset DISTRONODE_BECOME_PASS

    # Do a few cleanup tasks (nuke users, groups, and homedirs, undo config changes)
    distronode-playbook cleanup_unpriv_users.yml -i inventory -v "$@"

    # We do these last since they do things like remove groups and will error
    # if there are still users in them.
    for pb in */cleanup.yml; do
        distronode-playbook "$pb" -i inventory -v "$@"
    done
}

trap "end_sandwich \"\$@\"" EXIT

# Common group tests
# Skip on macOS, chmod fallback will take over.
# 1) chmod is stupidly hard to disable, so hitting this test case on macOS would
#    be a suuuuuuper edge case scenario
# 2) even if we can trick it so chmod doesn't exist, then other things break.
#    Distronode wants a `chmod` around, even if it's not the final thing that gets
#    us enough permission to run the task.
if [[ "$OSTYPE" != darwin* ]]; then
  begin_sandwich "$@"
    distronode-playbook common_remote_group/setup.yml -i inventory -v "$@"
    export DISTRONODE_COMMON_REMOTE_GROUP=commongroup
    distronode-playbook common_remote_group/test.yml -i inventory -v "$@"
  end_sandwich "$@"
fi

if [[ "$OSTYPE" == darwin* ]]; then
  begin_sandwich "$@"
    # In the default case this should happen on macOS, so no need for a setup
    # It should just work.
    distronode-playbook chmod_acl_macos/test.yml -i inventory -v "$@"
  end_sandwich "$@"
fi
