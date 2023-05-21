from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.accounts.models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
        ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "phonenumber",
            "telegram_id",
        ]
