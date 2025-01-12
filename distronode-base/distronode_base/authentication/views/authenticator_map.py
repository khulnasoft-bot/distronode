from rest_framework.viewsets import ModelViewSet

from distronode_base.authentication.models import AuthenticatorMap
from distronode_base.authentication.serializers import AuthenticatorMapSerializer
from distronode_base.lib.utils.views.django_app_api import DistronodeBaseDjangoAppApiView


class AuthenticatorMapViewSet(DistronodeBaseDjangoAppApiView, ModelViewSet):
    """
    API endpoint that allows authenticator maps to be viewed or edited.
    """

    queryset = AuthenticatorMap.objects.all().order_by("id")
    serializer_class = AuthenticatorMapSerializer
