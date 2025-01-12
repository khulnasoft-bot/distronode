# Copyright: (c) 2022, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from distronode.plugins.action.normal import ActionModule as ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp, task_vars)
        result['action_plugin'] = 'vyos'

        return result
