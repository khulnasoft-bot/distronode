# Copyright (c) 2017 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
import sys
from io import BytesIO

import pytest

import distronode.module_utils.basic
from distronode.module_utils.common.text.converters import to_bytes
from collections.abc import MutableMapping


@pytest.fixture
def stdin(mocker, request):
    old_args = distronode.module_utils.basic._DISTRONODE_ARGS
    distronode.module_utils.basic._DISTRONODE_ARGS = None
    old_argv = sys.argv
    sys.argv = ['distronode_unittest']

    if isinstance(request.param, str):
        args = request.param
    elif isinstance(request.param, MutableMapping):
        if 'DISTRONODE_MODULE_ARGS' not in request.param:
            request.param = {'DISTRONODE_MODULE_ARGS': request.param}
        if '_distronode_remote_tmp' not in request.param['DISTRONODE_MODULE_ARGS']:
            request.param['DISTRONODE_MODULE_ARGS']['_distronode_remote_tmp'] = '/tmp'
        if '_distronode_keep_remote_files' not in request.param['DISTRONODE_MODULE_ARGS']:
            request.param['DISTRONODE_MODULE_ARGS']['_distronode_keep_remote_files'] = False
        args = json.dumps(request.param)
    else:
        raise Exception('Malformed data to the stdin pytest fixture')

    fake_stdin = BytesIO(to_bytes(args, errors='surrogate_or_strict'))

    mocker.patch('distronode.module_utils.basic.sys.stdin', mocker.MagicMock())
    mocker.patch('distronode.module_utils.basic.sys.stdin.buffer', fake_stdin)

    yield fake_stdin

    distronode.module_utils.basic._DISTRONODE_ARGS = old_args
    sys.argv = old_argv


@pytest.fixture
def am(stdin, request):
    old_args = distronode.module_utils.basic._DISTRONODE_ARGS
    distronode.module_utils.basic._DISTRONODE_ARGS = None
    old_argv = sys.argv
    sys.argv = ['distronode_unittest']

    argspec = {}
    if hasattr(request, 'param'):
        if isinstance(request.param, dict):
            argspec = request.param

    am = distronode.module_utils.basic.DistronodeModule(
        argument_spec=argspec,
    )
    am._name = 'distronode_unittest'

    yield am

    distronode.module_utils.basic._DISTRONODE_ARGS = old_args
    sys.argv = old_argv
