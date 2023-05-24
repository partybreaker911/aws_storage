from django.contrib import admin

from apps.storage.models import Folder, File, FileSignature, FileShare

admin.site.register(Folder)


class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ["id", "name", "timestamp"]


admin.site.register(File, FileAdmin)
admin.site.register(FileShare)
admin.site.register(FileSignature)
