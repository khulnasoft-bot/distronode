# -*- coding: utf-8 -*-
# Copyright (c) 2020 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


import logging
import sys


def test_logger():
    """
    Avoid CVE-2019-14846 as 3rd party libs will disclose secrets when
    logging is set to DEBUG
    """

    # clear loaded modules to have unadultered test.
    for loaded in list(sys.modules.keys()):
        if 'distronode' in loaded:
            del sys.modules[loaded]

    # force logger to exist via config
    from distronode import constants as C
    C.DEFAULT_LOG_PATH = '/dev/null'

    # initialize logger
    from distronode.utils.display import logger

    assert logger.root.level != logging.DEBUG


def test_empty_logger():
    # clear loaded modules to have unadultered test.
    for loaded in list(sys.modules.keys()):
        if 'distronode' in loaded:
            del sys.modules[loaded]

    # force logger to exist via config
    from distronode import constants as C
    C.DEFAULT_LOG_PATH = ''

    # initialize logger
    from distronode.utils.display import logger

    assert logger is None
