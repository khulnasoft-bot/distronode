#!/usr/bin/python
from __future__ import annotations


DISTRONODE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'core'}

DOCUMENTATION = """
---
module: module1
short_description: module1 Test module
description:
    - module1 Test module
author:
    - Distronode Core Team
"""

EXAMPLES = """
"""

RETURN = """
"""


from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(
            desc=dict(type='str'),
        ),
    )

    results = dict(msg="you just ran me.mycoll2.module1", desc=module.params.get('desc'))

    module.exit_json(**results)


if __name__ == '__main__':
    main()
