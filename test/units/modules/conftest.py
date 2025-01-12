# Copyright (c) 2017 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json

import pytest

from distronode.module_utils.common.text.converters import to_bytes


@pytest.fixture
def patch_distronode_module(request, mocker):
    request.param = {'DISTRONODE_MODULE_ARGS': request.param}
    request.param['DISTRONODE_MODULE_ARGS']['_distronode_remote_tmp'] = '/tmp'
    request.param['DISTRONODE_MODULE_ARGS']['_distronode_keep_remote_files'] = False

    args = json.dumps(request.param)

    mocker.patch('distronode.module_utils.basic._DISTRONODE_ARGS', to_bytes(args))
