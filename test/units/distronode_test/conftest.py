from __future__ import annotations


import os
import pytest
import sys


@pytest.fixture(autouse=True, scope='session')
def inject_distronode_test():
    """Make distronode_test available on `sys.path` for unit testing distronode-test."""
    test_lib = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'lib')
    sys.path.insert(0, test_lib)
