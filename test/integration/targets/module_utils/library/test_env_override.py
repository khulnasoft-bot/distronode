#!/usr/bin/python
# Most of these names are only available via PluginLoader so pylint doesn't
# know they exist
# pylint: disable=no-name-in-module
from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule
from distronode.module_utils.json_utils import data
from distronode.module_utils.mork import data as mork_data

results = {"json_utils": data, "mork": mork_data}

DistronodeModule(argument_spec=dict()).exit_json(**results)
