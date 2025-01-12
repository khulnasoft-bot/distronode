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
from unittest.mock import mock_open, patch
from distronode.errors import DistronodeError
from distronode.parsing.yaml.objects import DistronodeBaseYAMLObject


class TestErrors(unittest.TestCase):

    def setUp(self):
        self.message = 'This is the error message'
        self.unicode_message = 'This is an error with \xf0\x9f\x98\xa8 in it'

        self.obj = DistronodeBaseYAMLObject()

    def test_basic_error(self):
        e = DistronodeError(self.message)
        self.assertEqual(e.message, self.message)
        self.assertEqual(repr(e), self.message)

    def test_basic_unicode_error(self):
        e = DistronodeError(self.unicode_message)
        self.assertEqual(e.message, self.unicode_message)
        self.assertEqual(repr(e), self.unicode_message)

    @patch.object(DistronodeError, '_get_error_lines_from_file')
    def test_error_with_kv(self, mock_method):
        """ This tests a task with both YAML and k=v syntax

        - lineinfile: line=foo path=bar
            line: foo

        An accurate error message and position indicator are expected.

        _get_error_lines_from_file() returns (target_line, prev_line)
        """

        self.obj.distronode_pos = ('foo.yml', 2, 1)

        mock_method.return_value = ['    line: foo\n', '- lineinfile: line=foo path=bar\n']

        e = DistronodeError(self.message, self.obj)
        self.assertEqual(
            e.message,
            ("This is the error message\n\nThe error appears to be in 'foo.yml': line 1, column 19, but may\nbe elsewhere in the "
             "file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n- lineinfile: line=foo path=bar\n"
             "                  ^ here\n\n"
             "There appears to be both 'k=v' shorthand syntax and YAML in this task. Only one syntax may be used.\n")
        )

    @patch.object(DistronodeError, '_get_error_lines_from_file')
    def test_error_with_object(self, mock_method):
        self.obj.distronode_pos = ('foo.yml', 1, 1)

        mock_method.return_value = ('this is line 1\n', '')
        e = DistronodeError(self.message, self.obj)

        self.assertEqual(
            e.message,
            ("This is the error message\n\nThe error appears to be in 'foo.yml': line 1, column 1, but may\nbe elsewhere in the file depending on the "
             "exact syntax problem.\n\nThe offending line appears to be:\n\n\nthis is line 1\n^ here\n")
        )

    def test_get_error_lines_from_file(self):
        m = mock_open()
        m.return_value.readlines.return_value = ['this is line 1\n']

        with patch('builtins.open', m):
            # this line will be found in the file
            self.obj.distronode_pos = ('foo.yml', 1, 1)
            e = DistronodeError(self.message, self.obj)
            self.assertEqual(
                e.message,
                ("This is the error message\n\nThe error appears to be in 'foo.yml': line 1, column 1, but may\nbe elsewhere in the file depending on "
                 "the exact syntax problem.\n\nThe offending line appears to be:\n\n\nthis is line 1\n^ here\n")
            )

            with patch('distronode.errors.to_text', side_effect=IndexError('Raised intentionally')):
                # raise an IndexError
                self.obj.distronode_pos = ('foo.yml', 2, 1)
                e = DistronodeError(self.message, self.obj)
                self.assertEqual(
                    e.message,
                    ("This is the error message\n\nThe error appears to be in 'foo.yml': line 2, column 1, but may\nbe elsewhere in the file depending on "
                     "the exact syntax problem.\n\n(specified line no longer in file, maybe it changed?)")
                )

        m = mock_open()
        m.return_value.readlines.return_value = ['this line has unicode \xf0\x9f\x98\xa8 in it!\n']

        with patch('builtins.open', m):
            # this line will be found in the file
            self.obj.distronode_pos = ('foo.yml', 1, 1)
            e = DistronodeError(self.unicode_message, self.obj)
            self.assertEqual(
                e.message,
                ("This is an error with \xf0\x9f\x98\xa8 in it\n\nThe error appears to be in 'foo.yml': line 1, column 1, but may\nbe elsewhere in the "
                 "file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\nthis line has unicode \xf0\x9f\x98\xa8 in it!\n^ "
                 "here\n")
            )

    def test_get_error_lines_error_in_last_line(self):
        m = mock_open()
        m.return_value.readlines.return_value = ['this is line 1\n', 'this is line 2\n', 'this is line 3\n']

        with patch('builtins.open', m):
            # If the error occurs in the last line of the file, use the correct index to get the line
            # and avoid the IndexError
            self.obj.distronode_pos = ('foo.yml', 4, 1)
            e = DistronodeError(self.message, self.obj)
            self.assertEqual(
                e.message,
                ("This is the error message\n\nThe error appears to be in 'foo.yml': line 4, column 1, but may\nbe elsewhere in the file depending on "
                 "the exact syntax problem.\n\nThe offending line appears to be:\n\nthis is line 2\nthis is line 3\n^ here\n")
            )

    def test_get_error_lines_error_empty_lines_around_error(self):
        """Test that trailing whitespace after the error is removed"""
        m = mock_open()
        m.return_value.readlines.return_value = ['this is line 1\n', 'this is line 2\n', 'this is line 3\n', '  \n', '   \n', ' ']

        with patch('builtins.open', m):
            self.obj.distronode_pos = ('foo.yml', 5, 1)
            e = DistronodeError(self.message, self.obj)
            self.assertEqual(
                e.message,
                ("This is the error message\n\nThe error appears to be in 'foo.yml': line 5, column 1, but may\nbe elsewhere in the file depending on "
                 "the exact syntax problem.\n\nThe offending line appears to be:\n\nthis is line 2\nthis is line 3\n^ here\n")
            )
