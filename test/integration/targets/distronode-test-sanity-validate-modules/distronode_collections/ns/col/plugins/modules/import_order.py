#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


from distronode.module_utils.basic import DistronodeModule

DOCUMENTATION = """
module: import_order
short_description: Import order test module
description: Import order test module.
author:
  - Distronode Core Team
"""

EXAMPLES = """#"""
RETURN = """"""


if __name__ == '__main__':
    module = DistronodeModule(argument_spec=dict())
    module.exit_json()
