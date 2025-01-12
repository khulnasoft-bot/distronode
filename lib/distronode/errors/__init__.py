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

import re
import traceback

from collections.abc import Sequence

from distronode.errors.yaml_strings import (
    YAML_COMMON_DICT_ERROR,
    YAML_COMMON_LEADING_TAB_ERROR,
    YAML_COMMON_PARTIALLY_QUOTED_LINE_ERROR,
    YAML_COMMON_UNBALANCED_QUOTES_ERROR,
    YAML_COMMON_UNQUOTED_COLON_ERROR,
    YAML_COMMON_UNQUOTED_VARIABLE_ERROR,
    YAML_POSITION_DETAILS,
    YAML_AND_SHORTHAND_ERROR,
)
from distronode.module_utils.common.text.converters import to_native, to_text


class DistronodeError(Exception):
    """
    This is the base class for all errors raised from Distronode code,
    and can be instantiated with two optional parameters beyond the
    error message to control whether detailed information is displayed
    when the error occurred while parsing a data file of some kind.

    Usage:

        raise DistronodeError('some message here', obj=obj, show_content=True)

    Where "obj" is some subclass of distronode.parsing.yaml.objects.DistronodeBaseYAMLObject,
    which should be returned by the DataLoader() class.
    """

    def __init__(self, message="", obj=None, show_content=True, suppress_extended_error=False, orig_exc=None):
        super(DistronodeError, self).__init__(message)

        self._show_content = show_content
        self._suppress_extended_error = suppress_extended_error
        self._message = to_native(message)
        self.obj = obj
        self.orig_exc = orig_exc

    @property
    def message(self):
        # we import this here to prevent an import loop problem,
        # since the objects code also imports distronode.errors
        from distronode.parsing.yaml.objects import DistronodeBaseYAMLObject

        message = [self._message]

        # Add from previous exceptions
        if self.orig_exc:
            message.append('. %s' % to_native(self.orig_exc))

        # Add from yaml to give specific file/line no
        if isinstance(self.obj, DistronodeBaseYAMLObject):
            extended_error = self._get_extended_error()
            if extended_error and not self._suppress_extended_error:
                message.append(
                    '\n\n%s' % to_native(extended_error)
                )

        return ''.join(message)

    @message.setter
    def message(self, val):
        self._message = val

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    def _get_error_lines_from_file(self, file_name, line_number):
        """
        Returns the line in the file which corresponds to the reported error
        location, as well as the line preceding it (if the error did not
        occur on the first line), to provide context to the error.
        """

        target_line = ''
        prev_line = ''

        with open(file_name, 'r') as f:
            lines = f.readlines()

            # In case of a YAML loading error, PyYAML will report the very last line
            # as the location of the error. Avoid an index error here in order to
            # return a helpful message.
            file_length = len(lines)
            if line_number >= file_length:
                line_number = file_length - 1

            # If target_line contains only whitespace, move backwards until
            # actual code is found. If there are several empty lines after target_line,
            # the error lines would just be blank, which is not very helpful.
            target_line = lines[line_number]
            while not target_line.strip():
                line_number -= 1
                target_line = lines[line_number]

            if line_number > 0:
                prev_line = lines[line_number - 1]

        return (target_line, prev_line)

    def _get_extended_error(self):
        """
        Given an object reporting the location of the exception in a file, return
        detailed information regarding it including:

          * the line which caused the error as well as the one preceding it
          * causes and suggested remedies for common syntax errors

        If this error was created with show_content=False, the reporting of content
        is suppressed, as the file contents may be sensitive (ie. vault data).
        """

        error_message = ''

        try:
            (src_file, line_number, col_number) = self.obj.distronode_pos
            error_message += YAML_POSITION_DETAILS % (src_file, line_number, col_number)
            if src_file not in ('<string>', '<unicode>') and self._show_content:
                (target_line, prev_line) = self._get_error_lines_from_file(src_file, line_number - 1)
                target_line = to_text(target_line)
                prev_line = to_text(prev_line)
                if target_line:
                    stripped_line = target_line.replace(" ", "")

                    # Check for k=v syntax in addition to YAML syntax and set the appropriate error position,
                    # arrow index
                    if re.search(r'\w+(\s+)?=(\s+)?[\w/-]+', prev_line):
                        error_position = prev_line.rstrip().find('=')
                        arrow_line = (" " * error_position) + "^ here"
                        error_message = YAML_POSITION_DETAILS % (src_file, line_number - 1, error_position + 1)
                        error_message += "\nThe offending line appears to be:\n\n%s\n%s\n\n" % (prev_line.rstrip(), arrow_line)
                        error_message += YAML_AND_SHORTHAND_ERROR
                    else:
                        arrow_line = (" " * (col_number - 1)) + "^ here"
                        error_message += "\nThe offending line appears to be:\n\n%s\n%s\n%s\n" % (prev_line.rstrip(), target_line.rstrip(), arrow_line)

                    # TODO: There may be cases where there is a valid tab in a line that has other errors.
                    if '\t' in target_line:
                        error_message += YAML_COMMON_LEADING_TAB_ERROR
                    # common error/remediation checking here:
                    # check for unquoted vars starting lines
                    if ('{{' in target_line and '}}' in target_line) and ('"{{' not in target_line or "'{{" not in target_line):
                        error_message += YAML_COMMON_UNQUOTED_VARIABLE_ERROR
                    # check for common dictionary mistakes
                    elif ":{{" in stripped_line and "}}" in stripped_line:
                        error_message += YAML_COMMON_DICT_ERROR
                    # check for common unquoted colon mistakes
                    elif (len(target_line) and
                            len(target_line) > 1 and
                            len(target_line) > col_number and
                            target_line[col_number] == ":" and
                            target_line.count(':') > 1):
                        error_message += YAML_COMMON_UNQUOTED_COLON_ERROR
                    # otherwise, check for some common quoting mistakes
                    else:
                        # FIXME: This needs to split on the first ':' to account for modules like lineinfile
                        # that may have lines that contain legitimate colons, e.g., line: 'i ALL= (ALL) NOPASSWD: ALL'
                        # and throw off the quote matching logic.
                        parts = target_line.split(":")
                        if len(parts) > 1:
                            middle = parts[1].strip()
                            match = False
                            unbalanced = False

                            if middle.startswith("'") and not middle.endswith("'"):
                                match = True
                            elif middle.startswith('"') and not middle.endswith('"'):
                                match = True

                            if (len(middle) > 0 and
                                    middle[0] in ['"', "'"] and
                                    middle[-1] in ['"', "'"] and
                                    target_line.count("'") > 2 or
                                    target_line.count('"') > 2):
                                unbalanced = True

                            if match:
                                error_message += YAML_COMMON_PARTIALLY_QUOTED_LINE_ERROR
                            if unbalanced:
                                error_message += YAML_COMMON_UNBALANCED_QUOTES_ERROR

        except (IOError, TypeError):
            error_message += '\n(could not open file to display line)'
        except IndexError:
            error_message += '\n(specified line no longer in file, maybe it changed?)'

        return error_message


class DistronodePromptInterrupt(DistronodeError):
    """User interrupt"""


class DistronodePromptNoninteractive(DistronodeError):
    """Unable to get user input"""


class DistronodeAssertionError(DistronodeError, AssertionError):
    """Invalid assertion"""
    pass


class DistronodeOptionsError(DistronodeError):
    """ bad or incomplete options passed """
    pass


class DistronodeRequiredOptionError(DistronodeOptionsError):
    """ bad or incomplete options passed """
    pass


class DistronodeParserError(DistronodeError):
    """ something was detected early that is wrong about a playbook or data file """
    pass


class DistronodeInternalError(DistronodeError):
    """ internal safeguards tripped, something happened in the code that should never happen """
    pass


class DistronodeRuntimeError(DistronodeError):
    """ distronode had a problem while running a playbook """
    pass


class DistronodeModuleError(DistronodeRuntimeError):
    """ a module failed somehow """
    pass


class DistronodeConnectionFailure(DistronodeRuntimeError):
    """ the transport / connection_plugin had a fatal error """
    pass


class DistronodeAuthenticationFailure(DistronodeConnectionFailure):
    """invalid username/password/key"""
    pass


class DistronodeCallbackError(DistronodeRuntimeError):
    """ a callback failure """
    pass


class DistronodeTemplateError(DistronodeRuntimeError):
    """A template related error"""
    pass


class DistronodeFilterError(DistronodeTemplateError):
    """ a templating failure """
    pass


class DistronodeLookupError(DistronodeTemplateError):
    """ a lookup failure """
    pass


class DistronodeUndefinedVariable(DistronodeTemplateError):
    """ a templating failure """
    pass


class DistronodeFileNotFound(DistronodeRuntimeError):
    """ a file missing failure """

    def __init__(self, message="", obj=None, show_content=True, suppress_extended_error=False, orig_exc=None, paths=None, file_name=None):

        self.file_name = file_name
        self.paths = paths

        if message:
            message += "\n"
        if self.file_name:
            message += "Could not find or access '%s'" % to_text(self.file_name)
        else:
            message += "Could not find file"

        if self.paths and isinstance(self.paths, Sequence):
            searched = to_text('\n\t'.join(self.paths))
            if message:
                message += "\n"
            message += "Searched in:\n\t%s" % searched

        message += " on the Distronode Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"

        super(DistronodeFileNotFound, self).__init__(message=message, obj=obj, show_content=show_content,
                                                  suppress_extended_error=suppress_extended_error, orig_exc=orig_exc)


# These Exceptions are temporary, using them as flow control until we can get a better solution.
# DO NOT USE as they will probably be removed soon.
# We will port the action modules in our tree to use a context manager instead.
class DistronodeAction(DistronodeRuntimeError):
    """ Base Exception for Action plugin flow control """

    def __init__(self, message="", obj=None, show_content=True, suppress_extended_error=False, orig_exc=None, result=None):

        super(DistronodeAction, self).__init__(message=message, obj=obj, show_content=show_content,
                                            suppress_extended_error=suppress_extended_error, orig_exc=orig_exc)
        if result is None:
            self.result = {}
        else:
            self.result = result


class DistronodeActionSkip(DistronodeAction):
    """ an action runtime skip"""

    def __init__(self, message="", obj=None, show_content=True, suppress_extended_error=False, orig_exc=None, result=None):
        super(DistronodeActionSkip, self).__init__(message=message, obj=obj, show_content=show_content,
                                                suppress_extended_error=suppress_extended_error, orig_exc=orig_exc, result=result)
        self.result.update({'skipped': True, 'msg': message})


class DistronodeActionFail(DistronodeAction):
    """ an action runtime failure"""
    def __init__(self, message="", obj=None, show_content=True, suppress_extended_error=False, orig_exc=None, result=None):
        super(DistronodeActionFail, self).__init__(message=message, obj=obj, show_content=show_content,
                                                suppress_extended_error=suppress_extended_error, orig_exc=orig_exc, result=result)
        self.result.update({'failed': True, 'msg': message, 'exception': traceback.format_exc()})


class _DistronodeActionDone(DistronodeAction):
    """ an action runtime early exit"""
    pass


class DistronodePluginError(DistronodeError):
    """ base class for Distronode plugin-related errors that do not need DistronodeError contextual data """
    def __init__(self, message=None, plugin_load_context=None):
        super(DistronodePluginError, self).__init__(message)
        self.plugin_load_context = plugin_load_context


class DistronodePluginRemovedError(DistronodePluginError):
    """ a requested plugin has been removed """
    pass


class DistronodePluginCircularRedirect(DistronodePluginError):
    """a cycle was detected in plugin redirection"""
    pass


class DistronodeCollectionUnsupportedVersionError(DistronodePluginError):
    """a collection is not supported by this version of Distronode"""
    pass


class DistronodeFilterTypeError(DistronodeTemplateError, TypeError):
    """ a Jinja filter templating failure due to bad type"""
    pass


class DistronodePluginNotFound(DistronodePluginError):
    """ Indicates we did not find an Distronode plugin """
    pass
