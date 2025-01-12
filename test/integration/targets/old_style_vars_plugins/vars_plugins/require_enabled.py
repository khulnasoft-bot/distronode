from __future__ import annotations

from distronode.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):
    REQUIRES_ENABLED = True

    def get_vars(self, loader, path, entities):
        return {'require_enabled': True}
