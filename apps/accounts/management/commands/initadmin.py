from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create an initial admin user if one does not exist"

    def handle(self, *args: Any, **options: Any) -> str | None:
        """
        Handle function to create an initial admin user if one does not exist.

        Args:
            args: arguments passed to the command
            options: options passed to the command

        Returns:
            str or None: a success message if the user is created, None otherwise
        """
        username = "admin"
        email = "admin@admin.com"
        password = "admin"
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS("Successfully created the init admin"))
        else:
            self.stdout.write(
                self.style.WARNING("The initial admin user is already exists")
            )
