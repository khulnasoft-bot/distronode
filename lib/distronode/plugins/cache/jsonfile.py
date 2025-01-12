# (c) 2014, Brian Coca, Josh Drake, et al
# (c) 2017 Distronode Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

DOCUMENTATION = """
    name: jsonfile
    short_description: JSON formatted files.
    description:
        - This cache uses JSON formatted, per host, files saved to the filesystem.
    version_added: "1.9"
    author: Distronode Core (@distronode-core)
    options:
      _uri:
        required: True
        description:
          - Path in which the cache plugin will save the JSON files
        env:
          - name: DISTRONODE_CACHE_PLUGIN_CONNECTION
        ini:
          - key: fact_caching_connection
            section: defaults
        type: path
      _prefix:
        description: User defined prefix to use when creating the JSON files
        env:
          - name: DISTRONODE_CACHE_PLUGIN_PREFIX
        ini:
          - key: fact_caching_prefix
            section: defaults
      _timeout:
        default: 86400
        description: Expiration timeout for the cache plugin data
        env:
          - name: DISTRONODE_CACHE_PLUGIN_TIMEOUT
        ini:
          - key: fact_caching_timeout
            section: defaults
        type: integer
"""

import codecs
import json

from distronode.parsing.ajson import DistronodeJSONEncoder, DistronodeJSONDecoder
from distronode.plugins.cache import BaseFileCacheModule


class CacheModule(BaseFileCacheModule):
    """
    A caching module backed by json files.
    """

    def _load(self, filepath):
        # Valid JSON is always UTF-8 encoded.
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f, cls=DistronodeJSONDecoder)

    def _dump(self, value, filepath):
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(value, cls=DistronodeJSONEncoder, sort_keys=True, indent=4))
