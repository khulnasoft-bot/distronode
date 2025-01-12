#!/usr/bin/python
from __future__ import annotations

results = {}
# Test that we are rooted correctly
# Following files:
#   module_utils/yak/zebra/foo.py
from distronode.module_utils.zebra import foo4

results['zebra'] = foo4.data

from distronode.module_utils.basic import DistronodeModule
DistronodeModule(argument_spec=dict()).exit_json(**results)
