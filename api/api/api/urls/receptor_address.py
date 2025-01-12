# Copyright (c) 2017 Distronode, Inc.
# All Rights Reserved.

from django.urls import re_path

from api.api.views import (
    ReceptorAddressesList,
    ReceptorAddressDetail,
)


urls = [
    re_path(r'^$', ReceptorAddressesList.as_view(), name='receptor_addresses_list'),
    re_path(r'^(?P<pk>[0-9]+)/$', ReceptorAddressDetail.as_view(), name='receptor_address_detail'),
]

__all__ = ['urls']
