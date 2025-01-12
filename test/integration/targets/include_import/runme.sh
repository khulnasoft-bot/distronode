#!/usr/bin/env bash

set -eux

export DISTRONODE_ROLES_PATH=./roles

function gen_task_files() {
    for i in $(printf "%03d " {1..39}); do
        echo -e "- name: Hello Message\n  debug:\n    msg: Task file ${i}" > "tasks/hello/tasks-file-${i}.yml"
    done
}

## Adhoc

distronode -m include_role -a name=role1 localhost

## Import (static)

# Playbook
distronode-playbook playbook/test_import_playbook.yml -i inventory "$@"

DISTRONODE_STRATEGY='linear' distronode-playbook playbook/test_import_playbook_tags.yml -i inventory "$@" --tags canary1,canary22,validate --skip-tags skipme

# Tasks
DISTRONODE_STRATEGY='linear' distronode-playbook tasks/test_import_tasks.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook tasks/test_import_tasks.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook tasks/test_import_tasks_tags.yml -i inventory "$@" --tags tasks1,canary1,validate

# Role
DISTRONODE_STRATEGY='linear' distronode-playbook role/test_import_role.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook role/test_import_role.yml -i inventory "$@"


## Include (dynamic)

# Tasks
DISTRONODE_STRATEGY='linear' distronode-playbook tasks/test_include_tasks.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook tasks/test_include_tasks.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook tasks/test_include_tasks_tags.yml -i inventory "$@" --tags tasks1,canary1,validate

# Role
DISTRONODE_STRATEGY='linear' distronode-playbook role/test_include_role.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook role/test_include_role.yml -i inventory "$@"

# https://github.com/distronode/distronode/issues/68515
distronode-playbook -v role/test_include_role_vars_from.yml 2>&1 | tee test_include_role_vars_from.out
test "$(grep -E -c 'Expected a string for vars_from but got' test_include_role_vars_from.out)" = 1

## Max Recursion Depth
# https://github.com/distronode/distronode/issues/23609
DISTRONODE_STRATEGY='linear' distronode-playbook test_role_recursion.yml -i inventory "$@"
DISTRONODE_STRATEGY='linear' distronode-playbook test_role_recursion_fqcn.yml -i inventory "$@"

## Nested tasks
# https://github.com/distronode/distronode/issues/34782
DISTRONODE_STRATEGY='linear' distronode-playbook test_nested_tasks.yml  -i inventory "$@"
DISTRONODE_STRATEGY='linear' distronode-playbook test_nested_tasks_fqcn.yml  -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook test_nested_tasks.yml  -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook test_nested_tasks_fqcn.yml  -i inventory "$@"

## Tons of top level include_tasks
# https://github.com/distronode/distronode/issues/36053
# Fixed by https://github.com/distronode/distronode/pull/36075
gen_task_files
DISTRONODE_STRATEGY='linear' distronode-playbook test_copious_include_tasks.yml  -i inventory "$@"
DISTRONODE_STRATEGY='linear' distronode-playbook test_copious_include_tasks_fqcn.yml  -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook test_copious_include_tasks.yml  -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook test_copious_include_tasks_fqcn.yml  -i inventory "$@"
rm -f tasks/hello/*.yml

# Included tasks should inherit attrs from non-dynamic blocks in parent chain
# https://github.com/distronode/distronode/pull/38827
DISTRONODE_STRATEGY='linear' distronode-playbook test_grandparent_inheritance.yml -i inventory "$@"
DISTRONODE_STRATEGY='linear' distronode-playbook test_grandparent_inheritance_fqcn.yml -i inventory "$@"

# undefined_var
DISTRONODE_STRATEGY='linear' distronode-playbook undefined_var/playbook.yml  -i inventory "$@"
DISTRONODE_STRATEGY='free' distronode-playbook undefined_var/playbook.yml  -i inventory "$@"

# include_ + apply (explicit inheritance)
DISTRONODE_STRATEGY='linear' distronode-playbook apply/include_apply.yml -i inventory "$@" --tags foo
set +e
OUT=$(DISTRONODE_STRATEGY='linear' distronode-playbook apply/import_apply.yml -i inventory "$@" --tags foo 2>&1 | grep 'ERROR! Invalid options for import_tasks: apply')
set -e
if [[ -z "$OUT" ]]; then
    echo "apply on import_tasks did not cause error"
    exit 1
fi

DISTRONODE_STRATEGY='linear' DISTRONODE_PLAYBOOK_VARS_ROOT=all distronode-playbook apply/include_apply_65710.yml -i inventory "$@"
DISTRONODE_STRATEGY='free' DISTRONODE_PLAYBOOK_VARS_ROOT=all distronode-playbook apply/include_apply_65710.yml -i inventory "$@"

# Test that duplicate items in loop are not deduped
DISTRONODE_STRATEGY='linear' distronode-playbook tasks/test_include_dupe_loop.yml -i inventory "$@" | tee test_include_dupe_loop.out
test "$(grep -c '"item=foo"' test_include_dupe_loop.out)" = 3
DISTRONODE_STRATEGY='free' distronode-playbook tasks/test_include_dupe_loop.yml -i inventory "$@" | tee test_include_dupe_loop.out
test "$(grep -c '"item=foo"' test_include_dupe_loop.out)" = 3

distronode-playbook public_exposure/playbook.yml -i inventory "$@"
distronode-playbook public_exposure/no_bleeding.yml -i inventory "$@"
distronode-playbook public_exposure/no_overwrite_roles.yml -i inventory "$@"

# https://github.com/distronode/distronode/pull/48068
DISTRONODE_HOST_PATTERN_MISMATCH=warning distronode-playbook run_once/playbook.yml "$@"

# https://github.com/distronode/distronode/issues/48936
distronode-playbook -v handler_addressing/playbook.yml 2>&1 | tee test_handler_addressing.out
test "$(grep -E -c 'include handler task|ERROR! The requested handler '"'"'do_import'"'"' was not found' test_handler_addressing.out)" = 2

# https://github.com/distronode/distronode/issues/49969
distronode-playbook -v parent_templating/playbook.yml 2>&1 | tee test_parent_templating.out
test "$(grep -E -c 'Templating the path of the parent include_tasks failed.' test_parent_templating.out)" = 0

# https://github.com/distronode/distronode/issues/54618
distronode-playbook test_loop_var_bleed.yaml "$@"

# https://github.com/distronode/distronode/issues/56580
distronode-playbook valid_include_keywords/playbook.yml "$@"

# https://github.com/distronode/distronode/issues/64902
distronode-playbook tasks/test_allow_single_role_dup.yml 2>&1 | tee test_allow_single_role_dup.out
test "$(grep -c 'ok=3' test_allow_single_role_dup.out)" = 1

# Test allow_duplicate with include_role and import_role
test "$(distronode-playbook tasks/test_dynamic_allow_dup.yml --tags include | grep -c 'Tasks file inside role')" = 2
test "$(distronode-playbook tasks/test_dynamic_allow_dup.yml --tags import | grep -c 'Tasks file inside role')" = 2

# test templating public, allow_duplicates, and rolespec_validate
distronode-playbook tasks/test_templating_IncludeRole_FA.yml 2>&1 | tee IncludeRole_FA_template.out
test "$(grep -c 'ok=6' IncludeRole_FA_template.out)" = 1
test "$(grep -c 'failed=0' IncludeRole_FA_template.out)" = 1

# https://github.com/distronode/distronode/issues/66764
DISTRONODE_HOST_PATTERN_MISMATCH=error distronode-playbook empty_group_warning/playbook.yml

distronode-playbook test_include_loop.yml "$@"
distronode-playbook test_include_loop_fqcn.yml "$@"

distronode-playbook include_role_omit/playbook.yml "$@"

# Test templating import_playbook, import_tasks, and import_role files
distronode-playbook playbook/test_templated_filenames.yml -e "pb=validate_templated_playbook.yml tasks=validate_templated_tasks.yml tasks_from=templated.yml" "$@" | tee out.txt
cat out.txt
test "$(grep out.txt -ce 'In imported playbook')" = 2
test "$(grep out.txt -ce 'In imported tasks')" = 3
test "$(grep out.txt -ce 'In imported role')" = 3

# https://github.com/distronode/distronode/issues/73657
distronode-playbook issue73657.yml 2>&1 | tee issue73657.out
test "$(grep -c 'SHOULD_NOT_EXECUTE' issue73657.out)" = 0

# https://github.com/distronode/distronode/issues/83874
distronode-playbook test_null_include_filename.yml 2>&1 | tee test_null_include_filename.out
test "$(grep -c 'ERROR! No file specified for distronode.builtin.include_tasks' test_null_include_filename.out)" = 1
test "$(grep -c 'The error appears to be in '\''.*/include_import/null_filename/tasks.yml'\'': line 4, column 3.*' test_null_include_filename.out)" = 1
test "$(grep -c '\- name: invalid include_task definition' test_null_include_filename.out)" = 1
