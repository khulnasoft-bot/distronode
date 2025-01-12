from __future__ import annotations

from distronode.plugins.vars import BaseVarsPlugin


class VarsModule(BaseVarsPlugin):
    # Implicitly
    # REQUIRES_ENABLED = False

    def get_vars(self, loader, path, entities):
        return {'auto_role_var': True}
