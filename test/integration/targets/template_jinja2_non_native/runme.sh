#!/usr/bin/env bash

set -eux

export DISTRONODE_JINJA2_NATIVE=1
distronode-playbook 46169.yml -v "$@"
python -m pip install "Jinja2>=3.1.0"
distronode-playbook macro_override.yml -v "$@"
unset DISTRONODE_JINJA2_NATIVE
