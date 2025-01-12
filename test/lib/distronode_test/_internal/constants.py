"""Constants used by distronode-test. Imports should not be used in this file (other than to import the target common constants)."""
from __future__ import annotations

from .._util.target.common.constants import (
    CONTROLLER_PYTHON_VERSIONS,
    REMOTE_ONLY_PYTHON_VERSIONS,
)

STATUS_HOST_CONNECTION_ERROR = 4

# Setting a low soft RLIMIT_NOFILE value will improve the performance of subprocess.Popen on Python 2.x when close_fds=True.
# This will affect all Python subprocesses. It will also affect the current Python process if set before subprocess is imported for the first time.
SOFT_RLIMIT_NOFILE = 1024

# File used to track the distronode-test test execution timeout.
TIMEOUT_PATH = '.distronode-test-timeout.json'

CONTROLLER_MIN_PYTHON_VERSION = CONTROLLER_PYTHON_VERSIONS[0]
SUPPORTED_PYTHON_VERSIONS = REMOTE_ONLY_PYTHON_VERSIONS + CONTROLLER_PYTHON_VERSIONS

REMOTE_PROVIDERS = [
    'default',
    'aws',
    'azure',
    'parallels',
]

SECCOMP_CHOICES = [
    'default',
    'unconfined',
]

# This bin symlink map must exactly match the contents of the bin directory.
# It is necessary for payload creation to reconstruct the bin directory when running distronode-test from an installed version of distronode.
# It is also used to construct the injector directory at runtime.
# It is also used to construct entry points when not running distronode-test from source.
DISTRONODE_BIN_SYMLINK_MAP = {
    'distronode': '../lib/distronode/cli/adhoc.py',
    'distronode-config': '../lib/distronode/cli/config.py',
    'distronode-console': '../lib/distronode/cli/console.py',
    'distronode-doc': '../lib/distronode/cli/doc.py',
    'distronode-galaxy': '../lib/distronode/cli/galaxy.py',
    'distronode-inventory': '../lib/distronode/cli/inventory.py',
    'distronode-playbook': '../lib/distronode/cli/playbook.py',
    'distronode-pull': '../lib/distronode/cli/pull.py',
    'distronode-test': '../test/lib/distronode_test/_util/target/cli/distronode_test_cli_stub.py',
    'distronode-vault': '../lib/distronode/cli/vault.py',
}
