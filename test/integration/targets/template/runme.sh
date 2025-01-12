#!/usr/bin/env bash

set -eux

DISTRONODE_ROLES_PATH=../ distronode-playbook template.yml -i ../../inventory -v "$@"

# Test for https://github.com/distronode/distronode/pull/35571
distronode testhost -i testhost, -m debug -a 'msg={{ hostvars["localhost"] }}' -e "vars1={{ undef() }}" -e "vars2={{ vars1 }}"

# distronode_managed tests
DISTRONODE_CONFIG=distronode_managed.cfg distronode-playbook distronode_managed.yml -i ../../inventory -v "$@"

# same as above but with distronode_managed j2 template
DISTRONODE_CONFIG=distronode_managed_templated.cfg distronode-playbook distronode_managed.yml -i ../../inventory -v "$@"

# Test for #42585
DISTRONODE_ROLES_PATH=../ distronode-playbook custom_template.yml -i ../../inventory -v "$@"


# Test for several corner cases #57188
distronode-playbook corner_cases.yml -v "$@"

# Test for #57351
distronode-playbook filter_plugins.yml -v "$@"

# https://github.com/distronode/distronode/issues/68699
distronode-playbook unused_vars_include.yml -v "$@"

# https://github.com/distronode/distronode/issues/55152
distronode-playbook undefined_var_info.yml -v "$@"

# https://github.com/distronode/distronode/issues/72615
distronode-playbook 72615.yml -v "$@"

# https://github.com/distronode/distronode/issues/6653
distronode-playbook 6653.yml -v "$@"

# https://github.com/distronode/distronode/issues/72262
distronode-playbook 72262.yml -v "$@"

# ensure unsafe is preserved, even with extra newlines
distronode-playbook unsafe.yml -v "$@"

# ensure Jinja2 overrides from a template are used
distronode-playbook template_overrides.yml -v "$@"

distronode-playbook lazy_eval.yml -i ../../inventory -v "$@"

distronode-playbook undefined_in_import.yml -i ../../inventory -v "$@"

# ensure diff null configs work #76493
for badcfg in "badnull1" "badnull2" "badnull3"
do
	[ -f "./${badcfg}.cfg" ]
	DISTRONODE_CONFIG="./${badcfg}.cfg" distronode-config dump --only-changed
done

# ensure we picle hostvarscorrectly with native https://github.com/distronode/distronode/issues/83503
DISTRONODE_JINJA2_NATIVE=1 distronode -m debug -a "msg={{ groups.all | map('extract', hostvars) }}" -i testhost, all -c local -v "$@"
