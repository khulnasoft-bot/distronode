# -*- mode: python -*-

# Copyright: (c) 2012, Jeroen Hoekx (@jhoekx)
# Copyright: Distronode Team
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = r"""
---
module: group_by
short_description: Create Distronode groups based on facts
extends_documentation_fragment:
  - action_common_attributes
  - action_common_attributes.conn
  - action_common_attributes.flow
  - action_core
description:
- Use facts to create ad-hoc groups that can be used later in a playbook.
- This module is also supported for Windows targets.
version_added: "0.9"
options:
  key:
    description:
    - The variables whose values will be used as groups.
    type: str
    required: true
  parents:
    description:
    - The list of the parent groups.
    type: list
    elements: str
    default: all
    version_added: "2.4"
attributes:
    action:
      support: full
    become:
      support: none
    bypass_host_loop:
      support: none
    bypass_task_loop:
      support: none
    check_mode:
      details: While this makes no changes to target systems the 'in memory' inventory will still be altered
      support: partial
    core:
      details: While parts of this action are implemented in core, other parts are still available as normal plugins and can be partially overridden
      support: partial
    connection:
        support: none
    delegation:
        support: none
    diff_mode:
      support: none
    platform:
        platforms: all
notes:
- Spaces in group names are converted to dashes '-'.
- Though this module does not change the remote host,
  we do provide 'changed' status as it can be useful
  for those trying to track inventory changes.
seealso:
- module: distronode.builtin.add_host
author:
- Jeroen Hoekx (@jhoekx)
"""

EXAMPLES = r"""
- name: Create groups based on the machine architecture
  distronode.builtin.group_by:
    key: machine_{{ distronode_machine }}

- name: Create groups like 'virt_kvm_host'
  distronode.builtin.group_by:
    key: virt_{{ distronode_virtualization_type }}_{{ distronode_virtualization_role }}

- name: Create nested groups
  distronode.builtin.group_by:
    key: el{{ distronode_distribution_major_version }}-{{ distronode_architecture }}
    parents:
      - el{{ distronode_distribution_major_version }}

- name: Add all active hosts to a static group
  distronode.builtin.group_by:
    key: done
"""
