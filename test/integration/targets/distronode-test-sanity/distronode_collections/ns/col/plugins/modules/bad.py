#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
module: bad
short_description: Bad test module
description: Bad test module.
author:
  - Distronode Core Team
"""

EXAMPLES = """
- bad:
"""

RETURN = """"""

from distronode.module_utils.basic import DistronodeModule
from distronode import constants  # intentionally trigger pylint distronode-bad-module-import error  # pylint: disable=unused-import


def main():
    module = DistronodeModule(
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
