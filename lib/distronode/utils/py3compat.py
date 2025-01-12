# -*- coding: utf-8 -*-
#
# (c) 2018, Toshio Kuratomi <a.badger@gmail.com>
# Copyright: Contributors to the Distronode project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import inspect
import os

from distronode.utils.display import Display


display = Display()


def __getattr__(name):
    if name != 'environ':
        raise AttributeError(name)

    caller = inspect.stack()[1]

    display.deprecated(
        (
            'distronode.utils.py3compat.environ is deprecated in favor of os.environ. '
            f'Accessed by {caller.filename} line number {caller.lineno}'
        ),
        version='2.20',
    )

    return os.environ
