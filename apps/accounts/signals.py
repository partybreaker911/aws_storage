from typing import Any
from ipware import get_client_ip

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from apps.accounts.models import Profile, UserGeoData, RSAKeyPair
from apps.accounts.utils.generate_rsa_key import generate_rsa_keys

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
        request = kwargs.get("request")
        if request:
            client_ip, is_routable = get_client_ip(request)
        else:
            client_ip = None
        user_geo_data = UserGeoData.objects.create(user=instance, ip_address=client_ip)
        user_geo_data.save()
