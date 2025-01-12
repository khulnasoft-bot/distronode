from django.urls import include, path

from distronode_base.rbac.api.router import router
from distronode_base.rbac.api.views import RoleMetadataView
from distronode_base.rbac.apps import DistronodeRBACConfig

app_name = DistronodeRBACConfig.label

api_version_urls = [
    path('', include(router.urls)),
    path(r'role_metadata/', RoleMetadataView.as_view(), name="role-metadata"),
]

root_urls = []

api_urls = []
