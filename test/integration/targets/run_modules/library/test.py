#!/usr/bin/python

from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule

module = DistronodeModule(argument_spec=dict())

module.exit_json(**{'tempdir': module._remote_tmp})
