#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
- key: "value"wrong
"""

EXAMPLES = """
- key: "value"wrong
"""

RETURN = """
- key: "value"wrong
"""

from distronode.module_utils.basic import DistronodeModule


def main():
    DistronodeModule(argument_spec=dict())


if __name__ == '__main__':
    main()
