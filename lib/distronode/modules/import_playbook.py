# -*- coding: utf-8 -*-

# Copyright:  Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = r"""
---
author: Distronode Core Team (@distronode)
module: import_playbook
short_description: Import a playbook
description:
  - Includes a file with a list of plays to be executed.
  - Files with a list of plays can only be included at the top level.
  - You cannot use this action inside a play.
version_added: "2.4"
options:
  free-form:
    description:
      - The name of the imported playbook is specified directly without any other option.
extends_documentation_fragment:
  - action_common_attributes
  - action_common_attributes.conn
  - action_common_attributes.flow
  - action_core
  - action_core.import
attributes:
    check_mode:
        support: full
    diff_mode:
        support: none
    platform:
        platforms: all
notes:
  - This is a core feature of Distronode, rather than a module, and cannot be overridden like a module.
seealso:
- module: distronode.builtin.import_role
- module: distronode.builtin.import_tasks
- module: distronode.builtin.include_role
- module: distronode.builtin.include_tasks
- ref: playbooks_reuse
  description: More information related to including and importing playbooks, roles and tasks.
"""

EXAMPLES = r"""
- hosts: localhost
  tasks:
    - distronode.builtin.debug:
        msg: play1

- name: Include a play after another play
  distronode.builtin.import_playbook: otherplays.yaml

- name: Set variables on an imported playbook
  distronode.builtin.import_playbook: otherplays.yml
  vars:
    service: httpd

- name: Include a playbook from a collection
  distronode.builtin.import_playbook: my_namespace.my_collection.my_playbook

- name: This DOES NOT WORK
  hosts: all
  tasks:
    - distronode.builtin.debug:
        msg: task1

    - name: This fails because I'm inside a play already
      distronode.builtin.import_playbook: stuff.yaml
"""

RETURN = r"""
# This module does not return anything except plays to execute.
"""
