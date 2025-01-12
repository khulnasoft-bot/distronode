from django.apps import AppConfig

from distronode_base.api_documentation.customizations import apply_authentication_customizations


class ApiDocumentationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'distronode_base.api_documentation'
    label = 'dab_api_documentation'

    def ready(self):
        from django.conf import settings

        if 'distronode_base.authentication' in settings.INSTALLED_APPS:
            apply_authentication_customizations()
