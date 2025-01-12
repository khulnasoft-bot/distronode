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

from yaml.constructor import SafeConstructor, ConstructorError
from yaml.nodes import MappingNode

from distronode import constants as C
from distronode.module_utils.common.text.converters import to_bytes, to_native
from distronode.parsing.yaml.objects import DistronodeMapping, DistronodeSequence, DistronodeUnicode, DistronodeVaultEncryptedUnicode
from distronode.parsing.vault import VaultLib
from distronode.utils.display import Display
from distronode.utils.unsafe_proxy import wrap_var

display = Display()


class DistronodeConstructor(SafeConstructor):
    def __init__(self, file_name=None, vault_secrets=None):
        self._distronode_file_name = file_name
        super(DistronodeConstructor, self).__init__()
        self._vaults = {}
        self.vault_secrets = vault_secrets or []
        self._vaults['default'] = VaultLib(secrets=self.vault_secrets)

    def construct_yaml_map(self, node):
        data = DistronodeMapping()
        yield data
        value = self.construct_mapping(node)
        data.update(value)
        data.distronode_pos = self._node_position_info(node)

    def construct_mapping(self, node, deep=False):
        # Most of this is from yaml.constructor.SafeConstructor.  We replicate
        # it here so that we can warn users when they have duplicate dict keys
        # (pyyaml silently allows overwriting keys)
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                                   "expected a mapping node, but found %s" % node.id,
                                   node.start_mark)
        self.flatten_mapping(node)
        mapping = DistronodeMapping()

        # Add our extra information to the returned value
        mapping.distronode_pos = self._node_position_info(node)

        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise ConstructorError("while constructing a mapping", node.start_mark,
                                       "found unacceptable key (%s)" % exc, key_node.start_mark)

            if key in mapping:
                msg = (u'While constructing a mapping from {1}, line {2}, column {3}, found a duplicate dict key ({0}).'
                       u' Using last defined value only.'.format(key, *mapping.distronode_pos))
                if C.DUPLICATE_YAML_DICT_KEY == 'warn':
                    display.warning(msg)
                elif C.DUPLICATE_YAML_DICT_KEY == 'error':
                    raise ConstructorError(context=None, context_mark=None,
                                           problem=to_native(msg),
                                           problem_mark=node.start_mark,
                                           note=None)
                else:
                    # when 'ignore'
                    display.debug(msg)

            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value

        return mapping

    def construct_yaml_str(self, node):
        # Override the default string handling function
        # to always return unicode objects
        value = self.construct_scalar(node)
        ret = DistronodeUnicode(value)

        ret.distronode_pos = self._node_position_info(node)

        return ret

    def construct_vault_encrypted_unicode(self, node):
        value = self.construct_scalar(node)
        b_ciphertext_data = to_bytes(value)
        # could pass in a key id here to choose the vault to associate with
        # TODO/FIXME: plugin vault selector
        vault = self._vaults['default']
        if vault.secrets is None:
            raise ConstructorError(context=None, context_mark=None,
                                   problem="found !vault but no vault password provided",
                                   problem_mark=node.start_mark,
                                   note=None)
        ret = DistronodeVaultEncryptedUnicode(b_ciphertext_data)
        ret.vault = vault
        ret.distronode_pos = self._node_position_info(node)
        return ret

    def construct_yaml_seq(self, node):
        data = DistronodeSequence()
        yield data
        data.extend(self.construct_sequence(node))
        data.distronode_pos = self._node_position_info(node)

    def construct_yaml_unsafe(self, node):
        try:
            constructor = getattr(node, 'id', 'object')
            if constructor is not None:
                constructor = getattr(self, 'construct_%s' % constructor)
        except AttributeError:
            constructor = self.construct_object

        value = constructor(node)

        return wrap_var(value)

    def _node_position_info(self, node):
        # the line number where the previous token has ended (plus empty lines)
        # Add one so that the first line is line 1 rather than line 0
        column = node.start_mark.column + 1
        line = node.start_mark.line + 1

        # in some cases, we may have pre-read the data and then
        # passed it to the load() call for YAML, in which case we
        # want to override the default datasource (which would be
        # '<string>') to the actual filename we read in
        datasource = self._distronode_file_name or node.start_mark.name

        return (datasource, line, column)


DistronodeConstructor.add_constructor(
    u'tag:yaml.org,2002:map',
    DistronodeConstructor.construct_yaml_map)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'tag:yaml.org,2002:python/dict',
    DistronodeConstructor.construct_yaml_map)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'tag:yaml.org,2002:str',
    DistronodeConstructor.construct_yaml_str)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'tag:yaml.org,2002:python/unicode',
    DistronodeConstructor.construct_yaml_str)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'tag:yaml.org,2002:seq',
    DistronodeConstructor.construct_yaml_seq)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'!unsafe',
    DistronodeConstructor.construct_yaml_unsafe)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'!vault',
    DistronodeConstructor.construct_vault_encrypted_unicode)  # type: ignore[type-var]

DistronodeConstructor.add_constructor(
    u'!vault-encrypted',
    DistronodeConstructor.construct_vault_encrypted_unicode)  # type: ignore[type-var]
