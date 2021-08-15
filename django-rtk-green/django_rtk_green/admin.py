from django.contrib import admin

from django_rtk_green import models


class ActivationTokenAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]


class PasswordResetTokenAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]


admin.site.register(models.ActivationToken, ActivationTokenAdmin)
admin.site.register(models.PasswordResetToken, PasswordResetTokenAdmin)
