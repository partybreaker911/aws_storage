from django.urls import path

from apps.storage import views

app_name = "storage"

urlpatterns = [
    path("file/", views.FileUploadView.as_view(), name="file_upload"),
]
