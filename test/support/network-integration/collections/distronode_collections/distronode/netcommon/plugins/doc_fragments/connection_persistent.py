# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


class ModuleDocFragment(object):

    # Standard files documentation fragment
    DOCUMENTATION = r"""
options:
  import_modules:
    type: boolean
    description:
    - Reduce CPU usage and network module execution time
      by enabling direct execution. Instead of the module being packaged
      and executed by the shell, it will be directly executed by the Distronode
      control node using the same python interpreter as the Distronode process.
      Note- Incompatible with C(asynchronous mode).
      Note- Python 3 and Distronode 2.9.16 or greater required.
      Note- With Distronode 2.9.x fully qualified modules names are required in tasks.
    default: true
    ini:
    - section: distronode_network
      key: import_modules
    env:
    - name: DISTRONODE_NETWORK_IMPORT_MODULES
    vars:
    - name: distronode_network_import_modules
  persistent_connect_timeout:
    type: int
    description:
    - Configures, in seconds, the amount of time to wait when trying to initially
      establish a persistent connection.  If this value expires before the connection
      to the remote device is completed, the connection will fail.
    default: 30
    ini:
    - section: persistent_connection
      key: connect_timeout
    env:
    - name: DISTRONODE_PERSISTENT_CONNECT_TIMEOUT
    vars:
    - name: distronode_connect_timeout
  persistent_command_timeout:
    type: int
    description:
      - Configures, in seconds, the amount of time to wait for a command to
        return from the remote device.  If this timer is exceeded before the
        command returns, the connection plugin will raise an exception and
        close.
    default: 30
    ini:
      - section: persistent_connection
        key: command_timeout
    env:
      - name: DISTRONODE_PERSISTENT_COMMAND_TIMEOUT
    vars:
      - name: distronode_command_timeout
  persistent_log_messages:
    type: boolean
    description:
      - This flag will enable logging the command executed and response received from
        target device in the distronode log file. For this option to work 'log_path' distronode
        configuration option is required to be set to a file path with write access.
      - Be sure to fully understand the security implications of enabling this
        option as it could create a security vulnerability by logging sensitive information in log file.
    default: False
    ini:
      - section: persistent_connection
        key: log_messages
    env:
      - name: DISTRONODE_PERSISTENT_LOG_MESSAGES
    vars:
      - name: distronode_persistent_log_messages
"""
