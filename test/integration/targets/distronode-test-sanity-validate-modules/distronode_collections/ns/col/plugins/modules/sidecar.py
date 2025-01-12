#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule


if __name__ == '__main__':
    module = DistronodeModule(argument_spec=dict(
        test=dict(type='str', choices=['foo', 'bar'], default='foo'),
    ))
    module.exit_json(test='foo')
