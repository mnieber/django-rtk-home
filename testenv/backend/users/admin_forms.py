from django import forms
from django.core.exceptions import ValidationError


class UserAdminForm(forms.ModelForm):
    def clean_accepts_terms(self):
        if not self.cleaned_data["accepts_terms"]:
            raise ValidationError("Users must accept the terms.")
