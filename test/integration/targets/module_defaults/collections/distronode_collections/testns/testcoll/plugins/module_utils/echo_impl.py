from __future__ import annotations

import json
from distronode.module_utils import basic
from distronode.module_utils.basic import _load_params, DistronodeModule


def do_echo():
    p = _load_params()
    d = json.loads(basic._DISTRONODE_ARGS)
    d['DISTRONODE_MODULE_ARGS'] = {}
    basic._DISTRONODE_ARGS = json.dumps(d).encode('utf-8')
    module = DistronodeModule(argument_spec={})
    module.exit_json(args_in=p)
