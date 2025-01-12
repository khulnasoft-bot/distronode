#!/usr/bin/env bash

set -eux

# test no dupes when dependencies in b and c point to a in roles:
[ "$(distronode-playbook no_dupes.yml -i ../../inventory --tags inroles | grep -c '"msg": "A"')" = "1" ]
[ "$(distronode-playbook no_dupes.yml -i ../../inventory --tags acrossroles | grep -c '"msg": "A"')" = "1" ]
[ "$(distronode-playbook no_dupes.yml -i ../../inventory --tags intasks | grep -c '"msg": "A"')" = "1" ]

# but still dupe across plays
[ "$(distronode-playbook no_dupes.yml -i ../../inventory | grep -c '"msg": "A"')" = "3" ]

# and don't dedupe before the role successfully completes
[ "$(distronode-playbook role_complete.yml -i ../../inventory -i fake, --tags conditional_skipped | grep -c '"msg": "A"')" = "1" ]
[ "$(distronode-playbook role_complete.yml -i ../../inventory -i fake, --tags conditional_failed | grep -c '"msg": "failed_when task succeeded"')" = "1" ]
[ "$(distronode-playbook role_complete.yml -i ../../inventory -i fake, --tags unreachable -vvv | grep -c '"data": "reachable"')" = "1" ]
distronode-playbook role_complete.yml -i ../../inventory -i fake, --tags unreachable | grep -e 'ignored=2'

# include/import can execute another instance of role
[ "$(distronode-playbook allowed_dupes.yml -i ../../inventory --tags importrole | grep -c '"msg": "A"')" = "2" ]
[ "$(distronode-playbook allowed_dupes.yml -i ../../inventory --tags includerole | grep -c '"msg": "A"')" = "2" ]

[ "$(distronode-playbook dupe_inheritance.yml -i ../../inventory | grep -c '"msg": "abc"')" = "3" ]

# ensure role data is merged correctly
distronode-playbook data_integrity.yml -i ../../inventory "$@"

# ensure role fails when trying to load 'non role' in  _from
test_no_outside=("no_outside.yml" "no_outside_import.yml")
for file in "${test_no_outside[@]}"; do
  distronode-playbook "$file" -i ../../inventory > "${file}_output.log" 2>&1 || true
  if grep "as it is not inside the expected role path" "${file}_output.log" >/dev/null; then
    echo "Test passed for $file (playbook failed with expected output, output not shown)."
  else
    echo "Test failed for $file, expected output from playbook failure is missing, output not shown)."
    exit 1
  fi
done

# ensure subdir contained to role in tasks_from is valid
distronode-playbook test_subdirs.yml -i ../../inventory "$@"

# ensure vars scope is correct
distronode-playbook vars_scope.yml -i ../../inventory "$@"

# test nested includes get parent roles greater than a depth of 3
[ "$(distronode-playbook 47023.yml -i ../../inventory | grep '\<\(Default\|Var\)\>' | grep -c 'is defined')" = "2" ]

# ensure import_role called from include_role has the include_role in the dep chain
distronode-playbook role_dep_chain.yml -i ../../inventory "$@"

# global role privacy setting test, set to private, set to not private, default
DISTRONODE_PRIVATE_ROLE_VARS=1 distronode-playbook privacy.yml -e @vars/privacy_vars.yml "$@"
DISTRONODE_PRIVATE_ROLE_VARS=0 distronode-playbook privacy.yml -e @vars/privacy_vars.yml "$@"
distronode-playbook privacy.yml -e @vars/privacy_vars.yml "$@"

for strategy in linear free; do
  [ "$(DISTRONODE_STRATEGY=$strategy distronode-playbook end_role.yml | grep -c CHECKPOINT)" = "1" ]
  [ "$(DISTRONODE_STRATEGY=$strategy distronode-playbook -i host1,host2 end_role_nested.yml | grep -c CHECKPOINT)" = "4" ]
done

[ "$(distronode localhost -m meta -a end_role 2>&1 | grep -c "ERROR! Cannot execute 'end_role' from outside of a role")" = "1" ]
[ "$(distronode-playbook end_role_handler_error.yml 2>&1 | grep -c "ERROR! Cannot execute 'end_role' from a handler")" = "1" ]
