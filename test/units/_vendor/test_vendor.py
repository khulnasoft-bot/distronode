# (c) 2020 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import annotations

import os
import pkgutil
import pytest
import sys

from unittest.mock import patch


def reset_internal_vendor_package():
    import distronode
    distronode_vendor_path = os.path.join(os.path.dirname(distronode.__file__), '_vendor')

    list(map(sys.path.remove, [path for path in sys.path if path == distronode_vendor_path]))

    for pkg in ['distronode._vendor', 'distronode']:
        sys.modules.pop(pkg, None)


def test_package_path_masking():
    from distronode import _vendor

    assert hasattr(_vendor, '__path__') and _vendor.__path__ == []


def test_no_vendored():
    reset_internal_vendor_package()
    with patch.object(pkgutil, 'iter_modules', return_value=[]):
        previous_path = list(sys.path)
        import distronode
        distronode_vendor_path = os.path.join(os.path.dirname(distronode.__file__), '_vendor')

        assert distronode_vendor_path not in sys.path
        assert sys.path == previous_path


def test_vendored(vendored_pkg_names=None):
    if not vendored_pkg_names:
        vendored_pkg_names = ['boguspkg']
    reset_internal_vendor_package()
    with patch.object(pkgutil, 'iter_modules', return_value=list((None, p, None) for p in vendored_pkg_names)):
        previous_path = list(sys.path)
        import distronode
        distronode_vendor_path = os.path.join(os.path.dirname(distronode.__file__), '_vendor')
        assert sys.path[0] == distronode_vendor_path
        assert sys.path[1:] == previous_path


def test_vendored_conflict():
    with pytest.warns(UserWarning) as w:
        test_vendored(vendored_pkg_names=['sys', 'pkgutil'])  # pass a real package we know is already loaded
        assert any(list('pkgutil, sys' in str(msg.message) for msg in w))  # ensure both conflicting modules are listed and sorted
