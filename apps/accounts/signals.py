from typing import Any, Dict, Type
from ipware import get_client_ip

from django.urls import reverse
from django.http import HttpRequest
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

from allauth.account.signals import user_logged_in

from apps.accounts.tasks import send_telegram_message_task
from apps.accounts.utils.session_url import get_sessions_url
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
def update_user_geo_data(
    sender: Any, user: Any, request: Any, **kwargs: Dict[str, Any]
) -> None:
    """
    Updates the user's geo data upon login if it is a new user login.

    Args:
        sender: The sender of the signal.
        user: The user who logged in.
        request: The request object.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    # Check if the user is new
    if kwargs.get("created"):
        # Get the client's IP address and whether it's routable
        client_ip, is_routable = get_client_ip(request)
        # Create a new UserGeoData object for the user with their IP address
        UserGeoData.objects.create(user=user, ip_address=client_ip)
    else:
        # If the user isn't new, set their IP address to None
        client_ip = None


@receiver(post_save, sender=UserGeoData)
def track_geodata_history(
    sender: Type[UserGeoData], instance: UserGeoData, created: bool, **kwargs: Any
) -> None:
    """
    Signal receiver function that tracks the history of UserGeoData objects.

    :param sender: Type[UserGeoData]
        The model class of the object that sent the signal.
    :param instance: UserGeoData
        The actual instance of UserGeoData that was just saved.
    :param created: bool
        A boolean indicating whether the object was just created.
    :param **kwargs: Any
        Any additional keyword arguments passed to the signal.
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
def create_user_session(sender: Any, request: Any, user: Any, **kwargs: Any) -> None:
    """
    Creates a UserSession object when a user logs in.

    Args:
        sender (Any): The sender of the signal.
        request (Any): The request object.
        user (Any): The user object.
        **kwargs (Any): Additional keyword arguments.

    Returns:
        None
    """
    # Get the session object associated with the request.
    session = Session.objects.get(session_key=request.session.session_key)
    # Create a UserSession object with the given user and session.
    UserSession.objects.create(user=user, session=session)


@receiver(user_logged_in)
def send_telegram_message(
    sender: Any, request: HttpRequest, user: Any, **kwargs: Any
) -> None:
    """
    Sends a message to a user's Telegram account when they log in.

    Args:
        sender (Any): The sender of the signal.
        request (HttpRequest): The HTTP request.
        user (Any): The user who logged in.
        **kwargs (Any): Additional keyword arguments.

    Returns:
        None
    """
    # Build the URL for the sessions page.
    sessions_url = request.build_absolute_uri(reverse("accounts:sessions"))
    # Create the message to be sent to the user's Telegram account.
    message = f"{user.username} successfully logged in. You can check out sessions at {sessions_url} \n "
    # If the user has a Telegram ID, send the message.
    if user.user_profile.telegram_id is not None:
        send_telegram_message_task.delay(
            chat_id=user.user_profile.telegram_id, message=message
        )
    else:
        # Otherwise, do nothing.
        pass
