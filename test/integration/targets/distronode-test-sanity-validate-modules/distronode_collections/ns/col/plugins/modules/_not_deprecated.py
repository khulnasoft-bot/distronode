#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
module: _not_deprecated
short_description: This module is not deprecated
description: Its name has a leading underscore, but it is not deprecated.
author:
  - Distronode Core Team
"""

EXAMPLES = """#"""
RETURN = """"""

from distronode.module_utils.basic import DistronodeModule


if __name__ == '__main__':
    module = DistronodeModule(argument_spec=dict())
    module.exit_json()
