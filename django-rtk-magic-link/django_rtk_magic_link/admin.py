from django.contrib import admin

from django_rtk_magic_link import models


class MagicLinkTokenAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]


admin.site.register(models.MagicLinkToken, MagicLinkTokenAdmin)
