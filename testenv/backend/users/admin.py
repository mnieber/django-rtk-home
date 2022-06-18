from django.contrib import admin

from users import models
from users.admin_forms import UserAdminForm


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm

    def save_model(self, request, obj, form, change):
        models.User.objects.create_user(**form.cleaned_data)
