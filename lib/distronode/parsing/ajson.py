# Copyright: (c) 2018, Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json

# Imported for backwards compat
from distronode.module_utils.common.json import DistronodeJSONEncoder  # pylint: disable=unused-import

from distronode.parsing.vault import VaultLib
from distronode.parsing.yaml.objects import DistronodeVaultEncryptedUnicode
from distronode.utils.unsafe_proxy import wrap_var


class DistronodeJSONDecoder(json.JSONDecoder):

    _vaults = {}  # type: dict[str, VaultLib]

    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.object_hook
        super(DistronodeJSONDecoder, self).__init__(*args, **kwargs)

    @classmethod
    def set_secrets(cls, secrets):
        cls._vaults['default'] = VaultLib(secrets=secrets)

    def object_hook(self, pairs):
        for key in pairs:
            value = pairs[key]

            if key == '__distronode_vault':
                value = DistronodeVaultEncryptedUnicode(value)
                if self._vaults:
                    value.vault = self._vaults['default']
                return value
            elif key == '__distronode_unsafe':
                return wrap_var(value)

        return pairs
