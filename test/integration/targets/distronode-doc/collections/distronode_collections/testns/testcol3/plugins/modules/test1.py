#!/usr/bin/python
from __future__ import annotations


DOCUMENTATION = """
module: test1
short_description: Foo module in testcol3
description:
    - This is a foo module.
author:
    - me
"""

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(
        argument_spec=dict(),
    )

    module.exit_json()


if __name__ == '__main__':
    main()
