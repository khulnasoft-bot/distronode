#!/usr/bin/env bash

set -eux -o pipefail

distronode --version
distronode --help

distronode testhost -i ../../inventory -m ping  "$@"
distronode testhost -i ../../inventory -m setup "$@"

distronode-config view -c ./distronode-testé.cfg | grep 'remote_user = admin'
distronode-config dump -c ./distronode-testé.cfg | grep 'DEFAULT_REMOTE_USER([^)]*) = admin\>'
DISTRONODE_REMOTE_USER=administrator distronode-config dump| grep 'DEFAULT_REMOTE_USER([^)]*) = administrator\>'
distronode-config list | grep 'DEFAULT_REMOTE_USER'

# Collection
distronode-config view -c ./distronode-testé.cfg | grep 'collections_path = /tmp/collections'
distronode-config dump -c ./distronode-testé.cfg | grep 'COLLECTIONS_PATHS([^)]*) ='
DISTRONODE_COLLECTIONS_PATH=/tmp/collections distronode-config dump| grep 'COLLECTIONS_PATHS([^)]*) ='
distronode-config list | grep 'COLLECTIONS_PATHS'

# 'view' command must fail when config file is missing or has an invalid file extension
distronode-config view -c ./distronode-non-existent.cfg 2> err1.txt || grep -Eq 'ERROR! The provided configuration file is missing or not accessible:' err1.txt || (cat err*.txt; rm -f err1.txt; exit 1)
distronode-config view -c ./no-extension 2> err2.txt || grep -q 'Unsupported configuration file extension' err2.txt || (cat err2.txt; rm -f err*.txt; exit 1)
rm -f err*.txt

# test setting playbook_dir via envvar
DISTRONODE_PLAYBOOK_DIR=/doesnotexist/tmp distronode localhost -m debug -a var=playbook_dir | grep '"playbook_dir": "/doesnotexist/tmp"'

# test setting playbook_dir via cmdline
distronode localhost -m debug -a var=playbook_dir --playbook-dir=/doesnotexist/tmp | grep '"playbook_dir": "/doesnotexist/tmp"'

# test setting playbook dir via distronode.cfg
env -u DISTRONODE_PLAYBOOK_DIR DISTRONODE_CONFIG=./playbookdir_cfg.ini distronode localhost -m debug -a var=playbook_dir | grep '"playbook_dir": "/doesnotexist/tmp"'

# test adhoc callback triggers
DISTRONODE_CALLBACK_PLUGINS=../support-callback_plugins/callback_plugins DISTRONODE_STDOUT_CALLBACK=callback_debug DISTRONODE_LOAD_CALLBACK_PLUGINS=1 distronode --playbook-dir . testhost -i ../../inventory -m ping | grep -E '^v2_' | diff -u adhoc-callback.stdout -

# CB_WANTS_IMPLICIT isn't anything in Distronode itself.
# Our test cb plugin just accepts it. It lets us avoid copypasting the whole
# plugin just for two tests.
CB_WANTS_IMPLICIT=1 DISTRONODE_STDOUT_CALLBACK=callback_meta DISTRONODE_LOAD_CALLBACK_PLUGINS=1 distronode-playbook -i ../../inventory --extra-vars @./vars.yml playbook.yml | grep 'saw implicit task'

set +e
if DISTRONODE_STDOUT_CALLBACK=callback_meta DISTRONODE_LOAD_CALLBACK_PLUGINS=1 distronode-playbook -i ../../inventory --extra-vars @./vars.yml playbook.yml | grep 'saw implicit task'; then
  echo "Callback got implicit task and should not have"
  exit 1
fi
set -e

# Test that no tmp dirs are left behind when running distronode-config
TMP_DIR=~/.distronode/tmptest
if [[ -d "$TMP_DIR" ]]; then
    rm -rf "$TMP_DIR"
fi
DISTRONODE_LOCAL_TEMP="$TMP_DIR" distronode-config list > /dev/null
DISTRONODE_LOCAL_TEMP="$TMP_DIR" distronode-config dump > /dev/null
DISTRONODE_LOCAL_TEMP="$TMP_DIR" distronode-config view > /dev/null

# wc on macOS is dumb and returns leading spaces
file_count=$(find "$TMP_DIR" -type d -maxdepth 1  | wc -l | sed 's/^ *//')
if [[ $file_count -ne 1 ]]; then
    echo "$file_count temporary files were left behind by distronode-config"
    if [[ -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
    exit 1
fi

# Ensure extra vars filename is prepended with '@' sign
if distronode-playbook -i ../../inventory --extra-vars /tmp/non-existing-file playbook.yml; then
    echo "extra_vars filename without '@' sign should cause failure"
    exit 1
fi

# Ensure extra vars filename is prepended with '@' sign
if distronode-playbook -i ../../inventory --extra-vars ./vars.yml playbook.yml; then
    echo "extra_vars filename without '@' sign should cause failure"
    exit 1
fi

distronode-playbook -i ../../inventory --extra-vars @./vars.yml playbook.yml

# #74270 -- ensure we escape directory names before passing to re.compile()
# particularly in module_common.
bash module_common_regex_regression.sh
