# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = """
    name: remote_is_local
    short_description: remote is local
    description:
        - remote_is_local
    author: distronode (@core)
    version_added: historical
    extends_documentation_fragment:
        - connection_pipelining
    notes:
        - The remote user is ignored, the user with which the distronode CLI was executed is used instead.
"""


from distronode.plugins.connection.local import Connection as LocalConnection


class Connection(LocalConnection):
    _remote_is_local = True
