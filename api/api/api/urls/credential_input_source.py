# Copyright (c) 2019 Distronode, Inc.
# All Rights Reserved.

from django.urls import re_path

from api.api.views import CredentialInputSourceDetail, CredentialInputSourceList


urls = [
    re_path(r'^$', CredentialInputSourceList.as_view(), name='credential_input_source_list'),
    re_path(r'^(?P<pk>[0-9]+)/$', CredentialInputSourceDetail.as_view(), name='credential_input_source_detail'),
]

__all__ = ['urls']
