from django.urls import include, path
from rest_framework import routers

from distronode_base.activitystream import views

router = routers.SimpleRouter()
router.register(
    'activitystream',
    views.EntryReadOnlyViewSet,
    basename='activitystream',
)

api_version_urls = [path('', include(router.urls))]
