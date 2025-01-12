#!/usr/bin/env bash

set -eux

# ensure we execute su with a pseudo terminal
[ "$(distronode -a whoami --become-method=su localhost --become)" != "su: requires a terminal to execute" ]
