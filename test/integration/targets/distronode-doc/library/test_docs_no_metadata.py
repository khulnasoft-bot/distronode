#!/usr/bin/python
from __future__ import annotations


DOCUMENTATION = """
---
module: test_docs_no_metadata
short_description: Test module
description:
    - Test module
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
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
