from __future__ import annotations

from distronode.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        return dict(changed=False, failed=False, msg="action result should be masked", _distronode_no_log="yeppers")  # ensure that a truthy non-bool works here
