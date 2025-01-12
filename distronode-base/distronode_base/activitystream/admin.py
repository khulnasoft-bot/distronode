from django.contrib import admin

from distronode_base.activitystream.models import Entry
from distronode_base.lib.admin import ReadOnlyAdmin

admin.site.register(Entry, ReadOnlyAdmin)
