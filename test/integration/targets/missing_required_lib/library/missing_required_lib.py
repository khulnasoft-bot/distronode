#!/usr/bin/python
# Copyright: (c) 2020, Matt Martz <matt@sivel.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule, missing_required_lib

try:
    import distronode_missing_lib  # pylint: disable=unused-import
    HAS_LIB = True
except ImportError as e:
    HAS_LIB = False


def main():
    module = DistronodeModule({
        'url': {'type': 'bool'},
        'reason': {'type': 'bool'},
    })
    kwargs = {}
    if module.params['url']:
        kwargs['url'] = 'https://github.com/distronode/distronode'
    if module.params['reason']:
        kwargs['reason'] = 'for fun'
    if not HAS_LIB:
        module.fail_json(
            msg=missing_required_lib(
                'distronode_missing_lib',
                **kwargs
            ),
        )


if __name__ == '__main__':
    main()
