#!/usr/bin/python
from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule
# overridden
from distronode.module_utils.distronode_release import data

results = {"data": data}

DistronodeModule(argument_spec=dict()).exit_json(**results)
