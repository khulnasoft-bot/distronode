# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import sys

import pytest

from distronode import constants as C
from distronode.cli.arguments import option_helpers as opt_help
from distronode import __path__ as distronode_path
from distronode.release import __version__ as distronode_version

cpath = C.DEFAULT_MODULE_PATH

FAKE_PROG = u'distronode-cli-test'
VERSION_OUTPUT = opt_help.version(prog=FAKE_PROG)


@pytest.mark.parametrize(
    'must_have', [
        FAKE_PROG + u' [core %s]' % distronode_version,
        u'config file = %s' % C.CONFIG_FILE,
        u'configured module search path = %s' % cpath,
        u'distronode python module location = %s' % ':'.join(distronode_path),
        u'distronode collection location = %s' % ':'.join(C.COLLECTIONS_PATHS),
        u'executable location = ',
        u'python version = %s' % ''.join(sys.version.splitlines()),
    ]
)
def test_option_helper_version(must_have):
    assert must_have in VERSION_OUTPUT
