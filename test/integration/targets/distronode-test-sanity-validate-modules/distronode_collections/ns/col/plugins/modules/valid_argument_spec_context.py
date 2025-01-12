#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
module: valid_argument_spec_context
short_description: Valid argument spec context schema test module
description: Valid argument spec context schema test module
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
                context=dict(
                    extra_key='bar',
                ),
            ),
        ),
    )


if __name__ == '__main__':
    main()
