# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
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
from distronode.errors import DistronodeParserError
from distronode.playbook import Playbook
from distronode.vars.manager import VariableManager

from units.mock.loader import DictDataLoader


class TestPlaybook(unittest.TestCase):

    def test_empty_playbook(self):
        fake_loader = DictDataLoader({})
        p = Playbook(loader=fake_loader)

    def test_basic_playbook(self):
        fake_loader = DictDataLoader({
            "test_file.yml": """
            - hosts: all
            """,
        })
        p = Playbook.load("test_file.yml", loader=fake_loader)
        plays = p.get_plays()

    def test_bad_playbook_files(self):
        fake_loader = DictDataLoader({
            # represents a playbook which is not a list of plays
            "bad_list.yml": """
            foo: bar

            """,
            # represents a playbook where a play entry is mis-formatted
            "bad_entry.yml": """
            -
              - "This should be a mapping..."

            """,
        })
        vm = VariableManager()
        self.assertRaises(DistronodeParserError, Playbook.load, "bad_list.yml", vm, fake_loader)
        self.assertRaises(DistronodeParserError, Playbook.load, "bad_entry.yml", vm, fake_loader)
