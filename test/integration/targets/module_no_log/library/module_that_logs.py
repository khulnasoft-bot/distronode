#!/usr/bin/python
from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule


def main():
    module = DistronodeModule(argument_spec=dict(
        number=dict(type='int'),
    ))

    module.log('My number is: (%d)' % module.params['number'])
    module.exit_json()


if __name__ == '__main__':
    main()
