# -*- coding: utf-8 -*-
# Copyright (c) 2021 Distronode Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import annotations


class DistronodeFallbackNotFound(Exception):
    """Fallback validator was not found"""


class DistronodeValidationError(Exception):
    """Single argument spec validation error"""

    def __init__(self, message):
        super(DistronodeValidationError, self).__init__(message)
        self.error_message = message
        """The error message passed in when the exception was raised."""

    @property
    def msg(self):
        """The error message passed in when the exception was raised."""
        return self.args[0]


class DistronodeValidationErrorMultiple(DistronodeValidationError):
    """Multiple argument spec validation errors"""

    def __init__(self, errors=None):
        self.errors = errors[:] if errors else []
        """:class:`list` of :class:`DistronodeValidationError` objects"""

    def __getitem__(self, key):
        return self.errors[key]

    def __setitem__(self, key, value):
        self.errors[key] = value

    def __delitem__(self, key):
        del self.errors[key]

    @property
    def msg(self):
        """The first message from the first error in ``errors``."""
        return self.errors[0].args[0]

    @property
    def messages(self):
        """:class:`list` of each error message in ``errors``."""
        return [err.msg for err in self.errors]

    def append(self, error):
        """Append a new error to ``self.errors``.

        Only :class:`DistronodeValidationError` should be added.
        """

        self.errors.append(error)

    def extend(self, errors):
        """Append each item in ``errors`` to ``self.errors``. Only :class:`DistronodeValidationError` should be added."""
        self.errors.extend(errors)


class AliasError(DistronodeValidationError):
    """Error handling aliases"""


class ArgumentTypeError(DistronodeValidationError):
    """Error with parameter type"""


class ArgumentValueError(DistronodeValidationError):
    """Error with parameter value"""


class DeprecationError(DistronodeValidationError):
    """Error processing parameter deprecations"""


class ElementError(DistronodeValidationError):
    """Error when validating elements"""


class MutuallyExclusiveError(DistronodeValidationError):
    """Mutually exclusive parameters were supplied"""


class NoLogError(DistronodeValidationError):
    """Error converting no_log values"""


class RequiredByError(DistronodeValidationError):
    """Error with parameters that are required by other parameters"""


class RequiredDefaultError(DistronodeValidationError):
    """A required parameter was assigned a default value"""


class RequiredError(DistronodeValidationError):
    """Missing a required parameter"""


class RequiredIfError(DistronodeValidationError):
    """Error with conditionally required parameters"""


class RequiredOneOfError(DistronodeValidationError):
    """Error with parameters where at least one is required"""


class RequiredTogetherError(DistronodeValidationError):
    """Error with parameters that are required together"""


class SubParameterTypeError(DistronodeValidationError):
    """Incorrect type for subparameter"""


class UnsupportedError(DistronodeValidationError):
    """Unsupported parameters were supplied"""
