import os
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def get_file_size(file):
    """
    Get the size of a file in a human-readable format.

    Args:
        file (str): The path of the file to get the size of.

    Returns:
        str: The size of the file in a human-readable format, e.g. "42 Кб".

    Raises:
        OSError: If the file does not exist or cannot be accessed.

    Examples:
        >>> get_file_size('file.txt')
        '10 байт'
        >>> get_file_size('big_file.dat')
        '1.23 Гб'
    """
    size = os.path.getsize(file.path)
    if size < 1024:
        return f"{size} байт"
    elif size < 1024**2:
        return f"{round(size/1024, 2)} Кб"
    elif size < 1024**3:
        return f"{round(size/1024**2, 2)} Мб"
    else:
        return f"{round(size/1024**3, 2)} Гб"


class Folder(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="user_folders",
    )
    name = models.CharField(_("Name"), max_length=50)
    parent = models.ForeignKey(
        "self", verbose_name=_("Parent"), on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self) -> str:
        return f"{self.user}"


class File(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="user_files",
    )
    name = models.CharField(_("File name"), max_length=50)
    file = models.FileField(_("File"), upload_to="media/files/")
    folder = models.ForeignKey(
        Folder,
        verbose_name=_("Folder"),
        on_delete=models.CASCADE,
        null=True,
        related_name="files_folder",
    )
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self) -> str:
        return f"{self.name}"


class FileSignature(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    file = models.ForeignKey(
        File,
        verbose_name=_("File"),
        on_delete=models.CASCADE,
        related_name="file_signatures",
    )
    signature = models.TextField(_("Signature"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("File signature")
        verbose_name_plural = _("File signatures")

    def __str__(self) -> str:
        return f"{self.file}"
