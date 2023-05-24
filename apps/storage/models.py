import os
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import asymmetric
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from apps.accounts.models import RSAKeyPair

User = get_user_model()


def file_size(file):
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
    file = models.FileField(_("File"), upload_to="files/")
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

    # @property
    # def get_file_size(self):
    #     return f"{file_size(self.file)}"

    # def encrypt_and_sign(self):
    #     key_pair = RSAKeyPair.objects.get(user=self.user)
    #     public_key = key_pair.get_public_key()

    #     with self.file.open("rb") as f:
    #         file_data = f.read()

    #     # Encrypt the file using the public key
    #     encrypted_data = public_key.encrypt(
    #         file_data,
    #         padding.OAEP(
    #             mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #             algorithm=hashes.SHA256(),
    #             label=None,
    #         ),
    #     )

    #     # Save the encrypted file data
    #     encrypted_file_path = f"files/encrypted/{self.name}"
    #     with open(encrypted_file_path, "wb") as f:
    #         f.write(encrypted_data)

    #     # Generate the signature for the encrypted file
    #     private_key = key_pair.get_private_key()
    #     signer = private_key.signer(padding.PSS(mgf=padding.MGF1(hashes.SHA256())))
    #     signer.update(encrypted_data)
    #     signature = signer.finalize()

    #     # Save the file signature
    #     FileSignature.objects.create(file=self, signature=signature)

    #     return encrypted_file_path

    # def save(self, *args, **kwargs):
    #     is_new_file = not self.pk
    #     super().save(*args, **kwargs)

    #     if is_new_file:
    #         self.encrypt_and_sign()


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
