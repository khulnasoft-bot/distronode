#!/usr/bin/python
# https://github.com/distronode/distronode/issues/64664
# https://github.com/distronode/distronode/issues/64479

from __future__ import annotations

import sys

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule({})

    this_module = sys.modules[__name__]
    module.exit_json(
        failed=not getattr(this_module, 'DistronodeModule', False)
    )


if __name__ == '__main__':
    main()
