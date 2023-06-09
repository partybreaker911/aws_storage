import uuid

from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    last_login = models.DateTimeField(_("Last Login"), blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return f"{self.id}"


class Profile(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    middle_name = models.CharField(_("Middle Name"), max_length=50, blank=True)
    phonenumber = PhoneNumberField(_("Phone Number"), blank=True)
    telegram_id = models.CharField(_("Telegram ID"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self) -> str:
        return f"{self.user}"


class UserGeoData(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user_geo_data"
    )
    ip_address = models.GenericIPAddressField(_("IP"), blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True)
    country = models.CharField(_("Country"), max_length=50, blank=True)
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now_add=True, blank=True, null=True
    )

    class Meta:
        verbose_name = _("User Geo Data")
        verbose_name_plural = _("User Geo Data")

    def __str__(self) -> str:
        return f"{self.user}"


class UserGeoDataHistory(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="user_geo_data_history",
    )
    ip_address = models.GenericIPAddressField(_("IP"), blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True)
    country = models.CharField(_("Country"), max_length=50, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("User Geo Data History")
        verbose_name_plural = _("User Geo Data History")

    def __str__(self) -> str:
        return f"{self.user}"


class RSAKeyPair(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="rsa_key_pair"
    )
    public_key = models.TextField(_("Public Key"))
    private_key = models.TextField(_("Private Key"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("RSA Key Pair")
        verbose_name_plural = _("RSA Key Pairs")

    def __str__(self) -> str:
        return f"{self.id}"

    @property
    def get_public_key(self) -> serialization:
        """
        Returns the public key of the current instance as a `serialization.PublicKey` object.

        Args:
            self: The current instance.

        Returns:
            A `serialization.PublicKey` object representing the public key of the current instance.
        """
        return serialization.load_pem_public_key(
            self.public_key.encode(), backend=default_backend()
        )

    @property
    def get_private_key(self) -> serialization:
        """
        Return the private key as a RSAPrivateKey object.

        Args:
            self (object): The current instance of the class.

        Returns:
            RSAPrivateKey: The private key as a RSAPrivateKey object.
        """
        return serialization.load_pem_private_key(
            self.private_key.encode(), password=None, backend=default_backend()
        )


class UserSession(models.Model):
    id = models.UUIDField(
        _("ID"), primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_sessions"
    )
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("User Session")
        verbose_name_plural = _("User Sessions")

    def __str__(self) -> str:
        return f"{self.user.email}"
