from django.urls import path

from apps.storage import views

app_name = "storage"

urlpatterns = [
    path("file/", views.FileUploadView.as_view(), name="file_upload"),
    path("file/list/", views.FileListView.as_view(), name="file_list"),
    path("file/<uuid:pk>/detail", views.FileDetailView.as_view(), name="file_detail"),
    path("file/<uuid:pk>/share", views.FileShareView.as_view(), name="file_share"),
    path(
        "file/<uuid:pk>/unshare", views.FileUnshareView.as_view(), name="file_unshare"
    ),
    path("files/shared/", views.SharedFilesView.as_view(), name="file_shared"),
]
