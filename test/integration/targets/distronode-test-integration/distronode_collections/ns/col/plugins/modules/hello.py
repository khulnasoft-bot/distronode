#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
module: hello
short_description: Hello test module
description: Hello test module.
options:
  name:
    description: Name to say hello to.
    type: str
author:
  - Distronode Core Team
"""

EXAMPLES = """
- hello:
"""

RETURN = """"""

from distronode.module_utils.basic import DistronodeModule
from ..module_utils.my_util import hello


def main():
    module = DistronodeModule(
        argument_spec=dict(
            name=dict(type='str'),
        ),
    )

    module.exit_json(**say_hello(module.params['name']))


def say_hello(name):
    return dict(
        message=hello(name),
    )


if __name__ == '__main__':
    main()
