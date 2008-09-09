from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import BlockedIP, BlockedHost

class BlockedIPAdmin(admin.ModelAdmin):
    pass

class BlockedHostAdmin(admin.ModelAdmin):
    pass

admin.site.register(BlockedIP, BlockedIPAdmin)
admin.site.register(BlockedHost, BlockedHostAdmin)