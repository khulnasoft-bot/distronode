# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import platform

from distronode.galaxy import user_agent
from distronode.module_utils.distronode_release import __version__ as distronode_version


def test_user_agent():
    res = user_agent.user_agent()
    assert res.startswith('distronode-galaxy/%s' % distronode_version)
    assert platform.system() in res
    assert 'python:' in res
