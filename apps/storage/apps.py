from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StorageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.storage"
    verbose_name = _("Storage")

    def ready(self):
        try:
            import apps.storage.signals
        except ImportError:
            pass
