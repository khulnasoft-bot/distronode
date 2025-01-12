# Copyright (c), Toshio Kuratomi <tkuratomi@distronode.com> 2016
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

"""
.. warn:: Use distronode.module_utils.common.text.converters instead.
"""
from __future__ import annotations

# Backwards compat for people still calling it from this package
# pylint: disable=unused-import
import codecs

from distronode.module_utils.six import PY3, text_type, binary_type

from distronode.module_utils.common.text.converters import to_bytes, to_native, to_text
