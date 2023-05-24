from typing import Any
from django.db import models
from django.db.models.query import QuerySet
import rsa

from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import View, CreateView, DeleteView, ListView, DetailView
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.models import RSAKeyPair
from apps.storage.tasks import send_file_share_email
from apps.storage.models import Folder, File, FileSignature, FileShare
from apps.storage.forms import FileUploadForm, FileShareForm

from apps.storage.services.files import FileUploadService

User = get_user_model()


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


class FileListView(LoginRequiredMixin, ListView):
    model = File
    template_name = "storage/file_list.html"
    context_object_name = "files"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(user=self.request.user)


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    template_name = "storage/file_detail.html"
    context_object_name = "file"

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(user=self.request.user)


class FileShareView(LoginRequiredMixin, CreateView):
    model = FileShare
    form_class = FileShareForm
    template_name = "storage/file_share.html"

    def form_valid(self, form):
        file = get_object_or_404(File, id=self.kwargs["pk"], user=self.request.user)
        form.instance.file = file
        form.instance.user = form.cleaned_data["email"]
        response = super().form_valid(form)

        shared_user = form.cleaned_data["email"]
        file_url = self.request.build_absolute_uri(
            reverse("storage:file_detail", kwargs={"pk": file.id})
        )
        recepient_email = shared_user.email
        send_file_share_email.delay(file_url, recepient_email)
        return response

    def get_success_url(self):
        return reverse_lazy("storage:file_detail", kwargs={"pk": self.kwargs["pk"]})


class FileUnshareView(LoginRequiredMixin, DeleteView):
    model = FileShare
    template_name = "storage/file_unshare.html"

    def get_object(self, queryser=None) -> FileShare:
        """
        Retrieve a file shared by a user.

        Args:
            self (object): The object instance.
            queryser (None): An optional queryset.

        Returns:
            FileShare: The shared file.
        """
        file: File = get_object_or_404(
            File, id=self.kwargs["pk"], user=self.request.user
        )
        user: User = get_object_or_404(User, id=self.kwargs["user_id"])
        return get_object_or_404(FileShare, file=file, user=user)

    def get_success_url(self) -> str:
        """
        Get the success URL for the file detail view.

        Args:
            self: The instance of the view calling this function.

        Returns:
            A string representing the success URL.
        """
        return reverse_lazy("storage:file_detail", kwargs={"pk": self.kwargs["pk"]})
