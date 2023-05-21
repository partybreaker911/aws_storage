from typing import Any
from ipware import get_client_ip

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

from allauth.account.signals import user_logged_in

from apps.accounts.utils.generate_rsa_key import generate_rsa_keys
from apps.accounts.models import (
    Profile,
    UserGeoData,
    RSAKeyPair,
    UserGeoDataHistory,
    UserSession,
)

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_data(sender: Any, instance: User, created: bool, **kwargs: Any) -> None:
    """
    Creates a Profile and UserGeoData instance for the given User instance.

    Args:
        sender: The sender of the signal.
        instance: The User instance that was saved.
        created: A boolean indicating if the User instance was created.
        **kwargs: Additional keyword arguments.

    Returns:
        None.
    """
    if created:
        Profile.objects.create(user=instance)
        private_key, public_key = generate_rsa_keys()
        RSAKeyPair.objects.create(
            user=instance,
            public_key=public_key,
            private_key=private_key,
        )
        UserGeoData.objects.create(user=instance)


@receiver(user_logged_in)
def update_user_geo_data(sender, user, request, **kwargs) -> None:
    """
    Updates the user's geo data upon login if it is a new user login.
    """
    if kwargs.get("created"):
        client_ip, is_routable = get_client_ip(request)
        UserGeoData.objects.create(user=user, ip_address=client_ip)
    else:
        client_ip = None


@receiver(post_save, sender=UserGeoData)
def track_geodata_history(sender, instance, created, **kwargs):
    """
    Signal receiver function that tracks the history of UserGeoData objects.
    :param sender: The model class of the object that sent the signal.
    :param instance: The actual instance of UserGeoData that was just saved.
    :param created: A boolean indicating whether the object was just created.
    :param **kwargs: Any additional keyword arguments passed to the signal.
    :return: None
    """
    if created:
        UserGeoDataHistory.objects.create(
            user=instance.user,
            ip_address=instance.ip_address,
            city=instance.city,
            country=instance.country,
        )


@receiver(user_logged_in)
def create_user_session(sender, request, user, **kwargs):
    session = Session.objects.get(session_key=request.session.session_key)
    UserSession.objects.create(user=user, session=session)
