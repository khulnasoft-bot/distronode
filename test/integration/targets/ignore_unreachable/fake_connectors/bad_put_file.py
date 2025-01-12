from __future__ import annotations

import distronode.plugins.connection.local as distronode_local
from distronode.errors import DistronodeConnectionFailure

from distronode.utils.display import Display
display = Display()


class Connection(distronode_local.Connection):
    def put_file(self, in_path, out_path):
        display.debug('Intercepted call to send data')
        raise DistronodeConnectionFailure('BADLOCAL Error: this is supposed to fail')
