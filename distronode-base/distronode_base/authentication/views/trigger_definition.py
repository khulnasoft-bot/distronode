from rest_framework.response import Response

from distronode_base.authentication.utils.trigger_definition import TRIGGER_DEFINITION
from distronode_base.lib.utils.views.django_app_api import DistronodeBaseDjangoAppApiView


class TriggerDefinitionView(DistronodeBaseDjangoAppApiView):
    def get(self, request, format=None):
        return Response(TRIGGER_DEFINITION)
