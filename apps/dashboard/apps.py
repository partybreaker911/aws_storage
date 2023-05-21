from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    verbose_name = _("Dashboard")

    def ready(self) -> None:
        try:
            import apps.dashboard.signals
        except ImportError:
            pass
