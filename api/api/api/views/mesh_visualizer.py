# Copyright (c) 2018 Red Hat, Inc.
# All Rights Reserved.

from django.utils.translation import gettext_lazy as _

from api.api.generics import APIView, Response
from api.api.permissions import IsSystemAdminOrAuditor
from api.api.serializers import InstanceLinkSerializer, InstanceNodeSerializer
from api.main.models import InstanceLink, Instance


class MeshVisualizer(APIView):
    name = _("Mesh Visualizer")
    permission_classes = (IsSystemAdminOrAuditor,)
    swagger_topic = "System Configuration"

    def get(self, request, format=None):
        data = {
            'nodes': InstanceNodeSerializer(Instance.objects.all(), many=True).data,
            'links': InstanceLinkSerializer(InstanceLink.objects.select_related('target__instance', 'source'), many=True).data,
        }

        return Response(data)
