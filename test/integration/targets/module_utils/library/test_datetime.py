#!/usr/bin/python
# Most of these names are only available via PluginLoader so pylint doesn't
# know they exist
# pylint: disable=no-name-in-module
from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule
import datetime

module = DistronodeModule(argument_spec=dict(
    datetime=dict(type=str, required=True),
    date=dict(type=str, required=True),
))
result = {
    'datetime': datetime.datetime.strptime(module.params.get('datetime'), '%Y-%m-%dT%H:%M:%S'),
    'date': datetime.datetime.strptime(module.params.get('date'), '%Y-%m-%d').date(),
}
module.exit_json(**result)
