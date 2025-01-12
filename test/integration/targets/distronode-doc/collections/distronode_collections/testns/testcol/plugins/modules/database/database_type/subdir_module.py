#!/usr/bin/python
from __future__ import annotations


DOCUMENTATION = """
---
module: subdir_module
short_description: A module in multiple subdirectories
description:
    - A module in multiple subdirectories
author:
    - Distronode Core Team
version_added: 1.0.0
options: {}
"""

EXAMPLES = """
"""

RETURN = """
"""


from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
