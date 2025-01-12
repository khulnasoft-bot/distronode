from __future__ import annotations

from distronode.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        return {
            'remote_password': self._connection.get_option('remote_password'),
        }
