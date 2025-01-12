# (c) 2016, Adrian Likins <alikins@redhat.com>
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

import unittest
from units.mock.loader import DictDataLoader

from distronode import context
from distronode.inventory.manager import InventoryManager
from distronode.vars.manager import VariableManager

from distronode.cli.playbook import PlaybookCLI


class TestPlaybookCLI(unittest.TestCase):
    def test_flush_cache(self):
        cli = PlaybookCLI(args=["distronode-playbook", "--flush-cache", "foobar.yml"])
        cli.parse()
        self.assertTrue(context.CLIARGS['flush_cache'])

        variable_manager = VariableManager()
        fake_loader = DictDataLoader({'foobar.yml': ""})
        inventory = InventoryManager(loader=fake_loader, sources='testhost,')

        variable_manager.set_host_facts('testhost', {'canary': True})
        self.assertTrue('testhost' in variable_manager._fact_cache)

        cli._flush_cache(inventory, variable_manager)
        self.assertFalse('testhost' in variable_manager._fact_cache)
