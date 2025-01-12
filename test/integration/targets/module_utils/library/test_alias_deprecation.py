#!/usr/bin/python

from __future__ import annotations

from distronode.module_utils.basic import DistronodeModule
# overridden
from distronode.module_utils.distronode_release import data

results = {"data": data}

arg_spec = dict(
    foo=dict(type='str', aliases=['baz'], deprecated_aliases=[dict(name='baz', version='9.99')])
)

DistronodeModule(argument_spec=arg_spec).exit_json(**results)
