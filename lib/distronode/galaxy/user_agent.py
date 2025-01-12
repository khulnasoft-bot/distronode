# Copyright: (c) 2019, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import platform
import sys

from distronode.module_utils.distronode_release import __version__ as distronode_version


def user_agent():
    """Returns a user agent used by distronode-galaxy to include the Distronode version, platform and python version."""

    python_version = sys.version_info
    return u"distronode-galaxy/{distronode_version} ({platform}; python:{py_major}.{py_minor}.{py_micro})".format(
        distronode_version=distronode_version,
        platform=platform.system(),
        py_major=python_version.major,
        py_minor=python_version.minor,
        py_micro=python_version.micro,
    )
