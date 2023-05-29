from django.contrib import admin

from apps.storage.models import Folder, File, FileSignature, FileShare

admin.site.register(Folder)


class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = [
        "id",
        "name",
        "get_file_size",
        "timestamp",
    ]


admin.site.register(File, FileAdmin)


class FileShareAdmin(admin.ModelAdmin):
    model = FileShare
    list_display = [
        "user",
        "file",
        "timestamp",
    ]


admin.site.register(FileShare, FileShareAdmin)
admin.site.register(FileSignature)
