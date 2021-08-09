from django.contrib import admin

from dgr_setpasswordlater import models


admin.site.register(models.ActivationToken)
admin.site.register(models.PasswordResetToken)
