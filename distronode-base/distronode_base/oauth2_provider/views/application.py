from rest_framework.viewsets import ModelViewSet

from distronode_base.lib.utils.views.django_app_api import DistronodeBaseDjangoAppApiView
from distronode_base.lib.utils.views.permissions import IsSuperuserOrAuditor
from distronode_base.oauth2_provider.models import OAuth2Application
from distronode_base.oauth2_provider.permissions import OAuth2ScopePermission
from distronode_base.oauth2_provider.serializers import OAuth2ApplicationSerializer


class OAuth2ApplicationViewSet(DistronodeBaseDjangoAppApiView, ModelViewSet):
    queryset = OAuth2Application.objects.all()
    serializer_class = OAuth2ApplicationSerializer
    permission_classes = [OAuth2ScopePermission, IsSuperuserOrAuditor]
