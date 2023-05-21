from django.contrib import admin

from apps.storage.models import Folder, File, FileSignature

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(FileSignature)
