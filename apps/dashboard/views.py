from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.dashboard.services.dashboard import DashboardService


class DashboardView(LoginRequiredMixin, View):
    template_name = "dashboard/dashboard.html"

    def get(self, request):
        user = request.user
        files_for_user = DashboardService.get_files_for_user(user)
        count_files_for_user = DashboardService.count_files(user)
        context = {
            "files_for_user": files_for_user,
            "count_files_for_user": count_files_for_user,
        }
        return render(request, self.template_name, context)
