from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.storage.models import Folder, File, FileSignature
from apps.storage.forms import FileUploadForm
from apps.storage.services.files import FileUploadService


class FileUploadView(LoginRequiredMixin, View):
    template_name = "storage/file_upload.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handles GET requests to the view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        form = FileUploadForm()
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle HTTP POST requests.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.

        """
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            name = file.name
            user = request.user

            file_obj = FileUploadService.upload_file(user=user, name=name, file=file)
            return redirect("dashboard:dashboard")
        return render(request, self.template_name)
