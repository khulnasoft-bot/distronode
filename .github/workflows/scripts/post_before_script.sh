#!/usr/bin/env bash

set -mveuo pipefail
cmd_prefix bash -c "django-admin compilemessages"

echo "machine pulp
login admin
password password
" > ~/.netrc

chmod og-rw ~/.netrc

# Needed for the tests that write this out
cmd_prefix touch /distronode.cfg
cmd_prefix chown pulp:pulp /distronode.cfg
