from __future__ import annotations

import pkg_resources  # pylint: disable=unused-import

from distronode.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        return ['ok']
