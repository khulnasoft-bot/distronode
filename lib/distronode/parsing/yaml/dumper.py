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

import yaml

from distronode.module_utils.six import text_type, binary_type
from distronode.module_utils.common.yaml import SafeDumper
from distronode.parsing.yaml.objects import DistronodeUnicode, DistronodeSequence, DistronodeMapping, DistronodeVaultEncryptedUnicode
from distronode.utils.unsafe_proxy import DistronodeUnsafeText, DistronodeUnsafeBytes, NativeJinjaUnsafeText, NativeJinjaText
from distronode.template import DistronodeUndefined
from distronode.vars.hostvars import HostVars, HostVarsVars
from distronode.vars.manager import VarsWithSources


class DistronodeDumper(SafeDumper):
    """
    A simple stub class that allows us to add representers
    for our overridden object types.
    """


def represent_hostvars(self, data):
    return self.represent_dict(dict(data))


# Note: only want to represent the encrypted data
def represent_vault_encrypted_unicode(self, data):
    return self.represent_scalar(u'!vault', data._ciphertext.decode(), style='|')


def represent_unicode(self, data):
    return yaml.representer.SafeRepresenter.represent_str(self, text_type(data))


def represent_binary(self, data):
    return yaml.representer.SafeRepresenter.represent_binary(self, binary_type(data))


def represent_undefined(self, data):
    # Here bool will ensure _fail_with_undefined_error happens
    # if the value is Undefined.
    # This happens because Jinja sets __bool__ on StrictUndefined
    return bool(data)


DistronodeDumper.add_representer(
    DistronodeUnicode,
    represent_unicode,
)

DistronodeDumper.add_representer(
    DistronodeUnsafeText,
    represent_unicode,
)

DistronodeDumper.add_representer(
    DistronodeUnsafeBytes,
    represent_binary,
)

DistronodeDumper.add_representer(
    HostVars,
    represent_hostvars,
)

DistronodeDumper.add_representer(
    HostVarsVars,
    represent_hostvars,
)

DistronodeDumper.add_representer(
    VarsWithSources,
    represent_hostvars,
)

DistronodeDumper.add_representer(
    DistronodeSequence,
    yaml.representer.SafeRepresenter.represent_list,
)

DistronodeDumper.add_representer(
    DistronodeMapping,
    yaml.representer.SafeRepresenter.represent_dict,
)

DistronodeDumper.add_representer(
    DistronodeVaultEncryptedUnicode,
    represent_vault_encrypted_unicode,
)

DistronodeDumper.add_representer(
    DistronodeUndefined,
    represent_undefined,
)

DistronodeDumper.add_representer(
    NativeJinjaUnsafeText,
    represent_unicode,
)

DistronodeDumper.add_representer(
    NativeJinjaText,
    represent_unicode,
)
