#!/usr/bin/env bash

set -eux -o pipefail

export DISTRONODE_DEPRECATION_WARNINGS=True

### check general config

# check for entry key valid, no deprecation
[ "$(DISTRONODE_CONFIG='entry_key_not_deprecated.cfg' distronode -m meta -a 'noop'  localhost 2>&1 | grep -c 'DEPRECATION')" -eq "0" ]

# check for entry key deprecation including the name of the option, must be defined to trigger
[ "$(DISTRONODE_CONFIG='entry_key_deprecated.cfg' distronode -m meta -a 'noop' localhost 2>&1 | grep -c "\[DEPRECATION WARNING\]: \[testing\]deprecated option.")" -eq "1" ]

# check for deprecation of entry itself, must be consumed to trigger
[ "$(DISTRONODE_TEST_ENTRY2=1 distronode -m debug -a 'msg={{q("config", "_Z_TEST_ENTRY_2")}}' localhost  2>&1 | grep -c 'DEPRECATION')" -eq "1" ]

# check for entry deprecation, just need key defined to trigger
[ "$(DISTRONODE_CONFIG='entry_key_deprecated2.cfg' distronode -m meta -a 'noop'  localhost 2>&1 | grep -c 'DEPRECATION')" -eq "1" ]


### check plugin config

# force use of the test plugin
export DISTRONODE_CACHE_PLUGIN_CONNECTION=/var/tmp
export DISTRONODE_CACHE_PLUGIN=notjsonfile

# check for plugin(s) config option and setting non deprecation
[ "$(DISTRONODE_CACHE_PLUGIN_TIMEOUT=1 distronode -m meta -a 'noop'  localhost --playbook-dir ./ 2>&1 | grep -c 'DEPRECATION')" -eq "0" ]

# check for plugin(s) config option setting deprecation
[ "$(DISTRONODE_NOTJSON_CACHE_PLUGIN_TIMEOUT=1 distronode -m meta -a 'noop'  localhost --playbook-dir ./ 2>&1 | grep -c 'DEPRECATION')" -eq "1" ]

# check for plugin(s) config option deprecation
[ "$(DISTRONODE_NOTJSON_CACHE_PLUGIN_REMOVEME=1 distronode -m meta -a 'noop'  localhost --playbook-dir ./ 2>&1 | grep -c 'DEPRECATION')" -eq "1" ]

# check for the module deprecation
[ "$(distronode-doc willremove --playbook-dir ./ | grep -c 'DEPRECATED')" -eq "1" ]

# check for the module option deprecation
[ "$(distronode-doc removeoption --playbook-dir ./ | grep -c 'deprecated:')" -eq "1" ]

# check for plugin deprecation
[ "$(distronode-doc -t cache notjsonfile --playbook-dir ./ | grep -c 'DEPRECATED:')" -eq "1" ]
