# (c) 2015, Distronode Inc,
#
# This file is part of Distronode
#
# Distronode is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Distronode is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Distronode.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

from distronode.errors import DistronodeAction, DistronodeActionFail
from distronode.executor.module_common import get_action_args_with_defaults
from distronode.module_utils.facts.system.pkg_mgr import PKG_MGRS
from distronode.plugins.action import ActionBase
from distronode.utils.display import Display
from distronode.utils.vars import combine_vars

display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    BUILTIN_PKG_MGR_MODULES = {manager['name'] for manager in PKG_MGRS}

    def run(self, tmp=None, task_vars=None):
        """ handler for package operations """

        self._supports_check_mode = True
        self._supports_async = True

        result = super(ActionModule, self).run(tmp, task_vars)

        module = self._task.args.get('use', 'auto')

        try:
            if module == 'auto':

                if self._task.delegate_to:
                    hosts_vars = task_vars['hostvars'][self._task.delegate_to]
                    tvars = combine_vars(self._task.vars, task_vars.get('delegated_vars', {}))
                else:
                    hosts_vars = task_vars
                    tvars = task_vars

                # use config
                module = tvars.get('distronode_package_use', None)

                if not module:
                    # no use, no config, get from facts
                    if hosts_vars.get('distronode_facts', {}).get('pkg_mgr', False):
                        facts = hosts_vars
                        pmgr = 'pkg_mgr'
                    else:
                        # we had no facts, so generate them
                        # very expensive step, we actually run fact gathering because we don't have facts for this host.
                        facts = self._execute_module(
                            module_name='distronode.legacy.setup',
                            module_args=dict(filter='distronode_pkg_mgr', gather_subset='!all'),
                            task_vars=task_vars,
                        )
                        if facts.get("failed", False):
                            raise DistronodeActionFail(
                                f"Failed to fetch distronode_pkg_mgr to determine the package action backend: {facts.get('msg')}",
                                result=facts,
                            )
                        pmgr = 'distronode_pkg_mgr'

                    try:
                        # actually get from facts
                        module = facts['distronode_facts'][pmgr]
                    except KeyError:
                        raise DistronodeActionFail('Could not detect a package manager. Try using the "use" option.')

            if module and module != 'auto':
                if not self._shared_loader_obj.module_loader.has_plugin(module):
                    raise DistronodeActionFail('Could not find a matching action for the "%s" package manager.' % module)
                else:
                    # run the 'package' module
                    new_module_args = self._task.args.copy()
                    if 'use' in new_module_args:
                        del new_module_args['use']

                    # get defaults for specific module
                    context = self._shared_loader_obj.module_loader.find_plugin_with_context(module, collection_list=self._task.collections)
                    new_module_args = get_action_args_with_defaults(
                        context.resolved_fqcn, new_module_args, self._task.module_defaults, self._templar,
                        action_groups=self._task._parent._play._action_groups
                    )

                    if module in self.BUILTIN_PKG_MGR_MODULES:
                        # prefix with distronode.legacy to eliminate external collisions while still allowing library/ override
                        module = 'distronode.legacy.' + module

                    display.vvvv("Running %s" % module)
                    result.update(self._execute_module(module_name=module, module_args=new_module_args, task_vars=task_vars, wrap_async=self._task.async_val))
            else:
                raise DistronodeActionFail('Could not detect which package manager to use. Try gathering facts or setting the "use" option.')

        except DistronodeAction as e:
            result.update(e.result)

        return result
