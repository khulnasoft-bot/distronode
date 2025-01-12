# Copyright (c) 2016 Distronode, Inc.
# All Rights Reserved.

from django.core.mail.backends.base import BaseEmailBackend


class APIBaseEmailBackend(BaseEmailBackend):
    def format_body(self, body):
        return body
