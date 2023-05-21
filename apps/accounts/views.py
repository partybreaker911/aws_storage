from django.contrib import messages
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_list_or_404

from apps.accounts.models import Profile, RSAKeyPair
from apps.accounts.forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        user_profile_form = ProfileForm(instance=user_profile)
        context = {
            "user_profile_form": user_profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_profile = Profile.objects.get(user=request.user.id)
        user_profile_form = ProfileForm(request.POST, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request, _("Your user profile has been updated."))
            return redirect("dashboard:dashboard")
        else:
            messages.error(request, _("There was an error updating your profile"))
            return render(
                request,
                self.template_name,
                {
                    "user_profile_form": user_profile_form,
                },
            )
