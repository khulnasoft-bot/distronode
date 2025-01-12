# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Matt Martz <matt@sivel.net>
# Copyright (C) 2016 Rackspace US, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

import runpy
import inspect
import json
import os
import subprocess
import sys

from contextlib import contextmanager

from distronode.executor.powershell.module_manifest import PSModuleDepFinder
from distronode.module_utils.basic import FILE_COMMON_ARGUMENTS, DistronodeModule
from distronode.module_utils.six import reraise
from distronode.module_utils.common.text.converters import to_bytes, to_text

from .utils import CaptureStd, find_executable, get_module_name_from_filename


DISTRONODE_MODULE_CONSTRUCTOR_ARGS = tuple(list(inspect.signature(DistronodeModule.__init__).parameters)[1:])


class DistronodeModuleCallError(RuntimeError):
    pass


class DistronodeModuleImportError(ImportError):
    pass


class DistronodeModuleNotInitialized(Exception):
    pass


class _FakeDistronodeModuleInit:
    def __init__(self):
        self.args = tuple()
        self.kwargs = {}
        self.called = False

    def __call__(self, *args, **kwargs):
        if args and isinstance(args[0], DistronodeModule):
            # Make sure, due to creative calling, that we didn't end up with
            # ``self`` in ``args``
            self.args = args[1:]
        else:
            self.args = args
        self.kwargs = kwargs
        self.called = True
        raise DistronodeModuleCallError('DistronodeModuleCallError')


def _fake_load_params():
    pass


@contextmanager
def setup_env(filename):
    # Used to clean up imports later
    pre_sys_modules = list(sys.modules.keys())

    fake = _FakeDistronodeModuleInit()
    module = __import__('distronode.module_utils.basic').module_utils.basic
    _original_init = module.DistronodeModule.__init__
    _original_load_params = module._load_params
    setattr(module.DistronodeModule, '__init__', fake)
    setattr(module, '_load_params', _fake_load_params)

    try:
        yield fake
    finally:
        setattr(module.DistronodeModule, '__init__', _original_init)
        setattr(module, '_load_params', _original_load_params)

        # Clean up imports to prevent issues with mutable data being used in modules
        for k in list(sys.modules.keys()):
            # It's faster if we limit to items in distronode.module_utils
            # But if this causes problems later, we should remove it
            if k not in pre_sys_modules and k.startswith('distronode.module_utils.'):
                del sys.modules[k]


def get_ps_argument_spec(filename, collection):
    fqc_name = get_module_name_from_filename(filename, collection)

    pwsh = find_executable('pwsh')
    if not pwsh:
        raise FileNotFoundError('Required program for PowerShell arg spec inspection "pwsh" not found.')

    module_path = os.path.join(os.getcwd(), filename)
    b_module_path = to_bytes(module_path, errors='surrogate_or_strict')
    with open(b_module_path, mode='rb') as module_fd:
        b_module_data = module_fd.read()

    ps_dep_finder = PSModuleDepFinder()
    ps_dep_finder.scan_module(b_module_data, fqn=fqc_name)

    # For ps_argspec.ps1 to compile Distronode.Basic it also needs the AddType module_util.
    ps_dep_finder._add_module(name=b"Distronode.ModuleUtils.AddType", ext=".psm1", fqn=None, optional=False, wrapper=False)

    util_manifest = json.dumps({
        'module_path': to_text(module_path, errors='surrogate_or_strict'),
        'distronode_basic': ps_dep_finder.cs_utils_module["Distronode.Basic"]['path'],
        'ps_utils': {name: info['path'] for name, info in ps_dep_finder.ps_modules.items()}
    })

    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ps_argspec.ps1')
    proc = subprocess.run(['pwsh', script_path, util_manifest], stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)

    if proc.returncode != 0:
        raise DistronodeModuleImportError("STDOUT:\n%s\nSTDERR:\n%s" % (proc.stdout, proc.stderr))

    kwargs = json.loads(proc.stdout)

    # the validate-modules code expects the options spec to be under the argument_spec key not options as set in PS
    kwargs['argument_spec'] = kwargs.pop('options', {})

    return kwargs['argument_spec'], kwargs


def get_py_argument_spec(filename, collection):
    name = get_module_name_from_filename(filename, collection)

    with setup_env(filename) as fake:
        try:
            with CaptureStd():
                runpy.run_module(name, run_name='__main__', alter_sys=True)
        except DistronodeModuleCallError:
            pass
        except BaseException as e:
            # we want to catch all exceptions here, including sys.exit
            reraise(DistronodeModuleImportError, DistronodeModuleImportError('%s' % e), sys.exc_info()[2])

        if not fake.called:
            raise DistronodeModuleNotInitialized()

    try:
        # Convert positional arguments to kwargs to make sure that all parameters are actually checked
        for arg, arg_name in zip(fake.args, DISTRONODE_MODULE_CONSTRUCTOR_ARGS):
            fake.kwargs[arg_name] = arg
        # for ping kwargs == {'argument_spec':{'data':{'type':'str','default':'pong'}}, 'supports_check_mode':True}
        argument_spec = fake.kwargs.get('argument_spec') or {}
        # If add_file_common_args is truish, add options from FILE_COMMON_ARGUMENTS when not present.
        # This is the only modification to argument_spec done by DistronodeModule itself, and which is
        # not caught by setup_env's DistronodeModule replacement
        if fake.kwargs.get('add_file_common_args'):
            for k, v in FILE_COMMON_ARGUMENTS.items():
                if k not in argument_spec:
                    argument_spec[k] = v
        return argument_spec, fake.kwargs
    except (TypeError, IndexError):
        return {}, {}
