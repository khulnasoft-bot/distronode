from django.contrib import admin

from distronode_base.authentication.models import Authenticator, AuthenticatorMap, AuthenticatorUser

admin.site.register(Authenticator)
admin.site.register(AuthenticatorMap)
admin.site.register(AuthenticatorUser)
