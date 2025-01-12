from django.apps import AppConfig

from distronode_base.rbac.permission_registry import permission_registry


class DistronodeRBACConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'distronode_base.rbac'
    label = 'dab_rbac'
    verbose_name = 'DAB shared RBAC'

    def ready(self):
        permission_registry.call_when_apps_ready(self.apps, self)
