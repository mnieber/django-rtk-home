from django.contrib import admin

from django_rtk_upfront import models


class ActivationTokenAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]


admin.site.register(models.ActivationToken, ActivationTokenAdmin)
