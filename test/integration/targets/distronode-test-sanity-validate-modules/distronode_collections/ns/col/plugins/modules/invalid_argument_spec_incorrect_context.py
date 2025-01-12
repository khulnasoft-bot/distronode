#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
module: invalid_argument_spec_incorrect_context
short_description: Invalid argument spec incorrect context schema test module
description: Invalid argument spec incorrect context schema test module
author:
  - Distronode Core Team
options:
  foo:
    description: foo
    type: str
"""

EXAMPLES = """#"""
RETURN = """"""

from distronode.module_utils.basic import DistronodeModule


def main():
    DistronodeModule(
        argument_spec=dict(
            foo=dict(
                type='str',
                context='bar',
            ),
        ),
    )


if __name__ == '__main__':
    main()
