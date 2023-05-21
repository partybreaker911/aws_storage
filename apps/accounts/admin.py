from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserChangeForm
    form = CustomUserCreationForm
    model = CustomUser
    list_display = [
        "email",
        "last_login",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
