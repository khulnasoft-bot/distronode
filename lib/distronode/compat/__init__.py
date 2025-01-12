# (c) 2014, Toshio Kuratomi <tkuratomi@distronode.com>
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

"""
Compat library for distronode.  This contains compatibility definitions for older python
When we need to import a module differently depending on python version, do it
here.  Then in the code we can simply import from compat in order to get what we want.
"""
from __future__ import annotations
