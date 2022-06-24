from django.contrib import admin

from django_rtk_password import models


class PasswordResetTokenAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]


admin.site.register(models.PasswordResetToken, PasswordResetTokenAdmin)
