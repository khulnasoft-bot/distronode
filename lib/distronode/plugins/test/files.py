# (c) 2015, Distronode, Inc
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

from os.path import isdir, isfile, isabs, exists, lexists, islink, samefile, ismount


class TestModule(object):
    """ Distronode file jinja2 tests """

    def tests(self):
        return {
            # file testing
            'directory': isdir,
            'is_dir': isdir,
            'file': isfile,
            'is_file': isfile,
            'link': islink,
            'is_link': islink,
            'exists': exists,
            'link_exists': lexists,

            # path testing
            'abs': isabs,
            'is_abs': isabs,
            'same_file': samefile,
            'is_same_file': samefile,
            'mount': ismount,
            'is_mount': ismount,
        }
