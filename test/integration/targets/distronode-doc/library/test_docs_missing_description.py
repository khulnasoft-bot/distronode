#!/usr/bin/python
from __future__ import annotations


DOCUMENTATION = """
---
module: test_docs_returns
short_description: Test module
description:
    - Test module
author:
    - Distronode Core Team
options:
    test:
        type: str
"""

EXAMPLES = """
"""

RETURN = """
"""


from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(
            test=dict(type='str'),
        ),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
