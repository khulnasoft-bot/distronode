from __future__ import annotations

import distronode.plugins.connection.local as distronode_local
from distronode.errors import DistronodeConnectionFailure

from distronode.utils.display import Display
display = Display()


class Connection(distronode_local.Connection):
    def exec_command(self, cmd, in_data=None, sudoable=True):
        display.debug('Intercepted call to exec remote command')
        raise DistronodeConnectionFailure('BADLOCAL Error: this is supposed to fail')
