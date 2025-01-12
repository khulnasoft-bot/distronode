#!/usr/bin/python

# Copyright: (c) 2021, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

DOCUMENTATION = r"""
---
module: distronode_release
short_description: Get distronode_release info from module_utils
description: Get distronode_release info from module_utils
author:
- Distronode Project
"""

EXAMPLES = r"""
#
"""

RETURN = r"""
#
"""

from distronode.module_utils.basic import DistronodeModule
from distronode.module_utils.distronode_release import __version__, __author__, __codename__


def main():
    module = DistronodeModule(argument_spec={})
    result = {
        'version': __version__,
        'author': __author__,
        'codename': __codename__,
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
