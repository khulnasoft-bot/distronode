#!/usr/bin/env bash

set -eux

ALOG=${OUTPUT_DIR}/distronode_log_test.log

# no log enabled
distronode-playbook logit.yml
# ensure file is not created
[ ! -f "${ALOG}" ]

# log enabled
DISTRONODE_LOG_PATH=${ALOG} distronode-playbook logit.yml
# ensure log file is created
[ -f "${ALOG}" ]
# Ensure tasks and log levels appear
grep -q '\[normal task\]' "${ALOG}"
grep -q 'INFO| TASK \[force warning\]' "${ALOG}"
grep -q 'WARNING| \[WARNING\]: conditional statements' "${ALOG}"
rm "${ALOG}"

# inline grep should fail if EXEC was present
set +e
DISTRONODE_LOG_PATH=${ALOG} DISTRONODE_LOG_VERBOSITY=3 distronode-playbook -v logit.yml | tee /dev/stderr | grep -q EXEC
rc=$?
set -e
if [ "$rc" == "0" ]; then
    false  # fail if we found EXEC in stdout
fi
grep -q EXEC "${ALOG}"

# Test that setting verbosity with no log won't crash
DISTRONODE_LOG_VERBOSITY=2 distronode-playbook logit.yml
