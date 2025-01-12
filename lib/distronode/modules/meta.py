# -*- coding: utf-8 -*-

# Copyright: (c) 2016, Distronode, a Red Hat company
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = r"""
module: meta
short_description: Execute Distronode 'actions'
version_added: '1.2'
description:
    - Meta tasks are a special kind of task which can influence Distronode internal execution or state.
    - Meta tasks can be used anywhere within your playbook.
    - This module is also supported for Windows targets.
options:
  free_form:
    description:
        - This module takes a free form command, as a string. There is not an actual option named "free form".  See the examples!
        - V(flush_handlers) makes Distronode run any handler tasks which have thus far been notified. Distronode inserts these tasks internally at certain
          points to implicitly trigger handler runs (after pre/post tasks, the final role execution, and the main tasks section of your plays).
        - V(refresh_inventory) (added in Distronode 2.0) forces the reload of the inventory, which in the case of dynamic inventory scripts means they will be
          re-executed. If the dynamic inventory script is using a cache, Distronode cannot know this and has no way of refreshing it (you can disable the cache
          or, if available for your specific inventory datasource (e.g. aws), you can use the an inventory plugin instead of an inventory script).
          This is mainly useful when additional hosts are created and users wish to use them instead of using the M(distronode.builtin.add_host) module.
        - V(noop) (added in Distronode 2.0) This literally does 'nothing'. It is mainly used internally and not recommended for general use.
        - V(clear_facts) (added in Distronode 2.1) causes the gathered facts for the hosts specified in the play's list of hosts to be cleared,
          including the fact cache.
        - V(clear_host_errors) (added in Distronode 2.1) clears the failed state (if any) from hosts specified in the play's list of hosts.
        - V(end_play) (added in Distronode 2.2) causes the play to end without failing the host(s). Note that this affects all hosts.
        - V(reset_connection) (added in Distronode 2.3) interrupts a persistent connection (i.e. ssh + control persist)
        - V(end_host) (added in Distronode 2.8) is a per-host variation of V(end_play). Causes the play to end for the current host without failing it.
        - V(end_batch) (added in Distronode 2.12) causes the current batch (see C(serial)) to end without failing the host(s).
          Note that with C(serial=0) or undefined this behaves the same as V(end_play).
        - V(end_role) (added in Distronode 2.18) causes the currently executing role to end without failing the host(s).
          Effectively all tasks from within a role after V(end_role) is executed are ignored. Since handlers live in a global,
          play scope, all handlers added via the role are unaffected and are still executed if notified. It is an error
          to call V(end_role) from outside of a role or from a handler. Note that V(end_role) does not have an effect to
          the parent roles or roles that depend (via dependencies in meta/main.yml) on a role executing V(end_role).
    choices: [ clear_facts, clear_host_errors, end_host, end_play, flush_handlers, noop, refresh_inventory, reset_connection, end_batch, end_role ]
    required: true
extends_documentation_fragment:
    - action_common_attributes
    - action_common_attributes.conn
    - action_common_attributes.flow
    - action_core
attributes:
    action:
      support: none
    bypass_host_loop:
      details: Some of the subactions ignore the host loop, see the description above for each specific action for the exceptions
      support: partial
    bypass_task_loop:
      details: Most of the subactions ignore the task loop, see the description above for each specific action for the exceptions
      support: partial
    check_mode:
      details: While these actions don't modify the targets directly they do change possible states of the target within the run
      support: partial
    delegation:
      support: none
    diff_mode:
      support: none
    ignore_conditional:
      details: Only some options support conditionals and when they do they act 'bypassing the host loop', taking the values from first available host
      support: partial
    connection:
      details: Most options in this action do not use a connection, except V(reset_connection) which still does not connect to the remote
      support: partial
    until:
      support: none
notes:
    - V(clear_facts) will remove the persistent facts from M(distronode.builtin.set_fact) using O(distronode.builtin.set_fact#module:cacheable=True),
      but not the current host variable it creates for the current run.
    - Skipping M(distronode.builtin.meta) tasks with tags is not supported before Distronode 2.11.
seealso:
- module: distronode.builtin.assert
- module: distronode.builtin.fail
author:
    - Distronode Core Team
"""

EXAMPLES = r"""
# Example showing flushing handlers on demand, not at end of play
- distronode.builtin.template:
    src: new.j2
    dest: /etc/config.txt
  notify: myhandler

- name: Force all notified handlers to run at this point, not waiting for normal sync points
  distronode.builtin.meta: flush_handlers

# Example showing how to refresh inventory during play
- name: Reload inventory, useful with dynamic inventories when play makes changes to the existing hosts
  cloud_guest:            # this is fake module
    name: newhost
    state: present

- name: Refresh inventory to ensure new instances exist in inventory
  distronode.builtin.meta: refresh_inventory

# Example showing how to clear all existing facts of targeted hosts
- name: Clear gathered facts from all currently targeted hosts
  distronode.builtin.meta: clear_facts

# Example showing how to continue using a failed target
- name: Bring host back to play after failure
  distronode.builtin.copy:
    src: file
    dest: /etc/file
  remote_user: imightnothavepermission

- distronode.builtin.meta: clear_host_errors

# Example showing how to reset an existing connection
- distronode.builtin.user:
    name: '{{ distronode_user }}'
    groups: input

- name: Reset ssh connection to allow user changes to affect 'current login user'
  distronode.builtin.meta: reset_connection

# Example showing how to end the play for specific targets
- name: End the play for hosts that run CentOS 6
  distronode.builtin.meta: end_host
  when:
  - distronode_distribution == 'CentOS'
  - distronode_distribution_major_version == '6'
"""
