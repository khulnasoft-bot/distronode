from __future__ import annotations

import json

import unittest
from unittest.mock import patch
from distronode.module_utils import basic
from distronode.module_utils.common.text.converters import to_bytes


def set_module_args(args):
    args['_distronode_remote_tmp'] = '/tmp'
    args['_distronode_keep_remote_files'] = False

    args = json.dumps({'DISTRONODE_MODULE_ARGS': args})
    basic._DISTRONODE_ARGS = to_bytes(args)


class DistronodeExitJson(Exception):
    pass


class DistronodeFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    raise DistronodeExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise DistronodeFailJson(kwargs)


class ModuleTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_module = patch.multiple(basic.DistronodeModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_module.start()
        self.mock_sleep = patch('time.sleep')
        self.mock_sleep.start()
        set_module_args({})
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_sleep.stop)
