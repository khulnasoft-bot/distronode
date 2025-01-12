# -*- coding: utf-8 -*-

# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2016, Toshio Kuratomi <tkuratomi@distronode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = """
---
module: ping
version_added: historical
short_description: Try to connect to host, verify a usable python and return C(pong) on success
description:
   - A trivial test module, this module always returns C(pong) on successful
     contact. It does not make sense in playbooks, but it is useful from
     C(/usr/bin/distronode) to verify the ability to login and that a usable Python is configured.
   - This is NOT ICMP ping, this is just a trivial test module that requires Python on the remote-node.
   - For Windows targets, use the M(distronode.windows.win_ping) module instead.
   - For Network targets, use the M(distronode.netcommon.net_ping) module instead.
options:
  data:
    description:
      - Data to return for the C(ping) return value.
      - If this parameter is set to C(crash), the module will cause an exception.
    type: str
    default: pong
seealso:
- module: distronode.netcommon.net_ping
- module: distronode.windows.win_ping
author:
    - Distronode Core Team
    - Michael DeHaan
"""

EXAMPLES = """
# Test we can logon to 'webservers' and execute python with json lib.
# distronode webservers -m ping

- name: Example from an Distronode Playbook
  ping:

- name: Induce an exception to see what happens
  ping:
    data: crash
"""

RETURN = """
ping:
    description: value provided with the data parameter
    returned: success
    type: str
    sample: pong
"""

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(
            data=dict(type='str', default='pong'),
        ),
        supports_check_mode=True
    )

    if module.params['data'] == 'crash':
        raise Exception("boom")

    result = dict(
        ping=module.params['data'],
    )

    module.exit_json(**result)


if __name__ == '__main__':
    main()
