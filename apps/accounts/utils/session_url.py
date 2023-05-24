from django.contrib.sites.models import Site
from django.urls import reverse


def get_sessions_url() -> str:
    """
    Returns the URL for the user sessions view on the current site.
    """
    # Get the current site
    current_site = Site.objects.get_current()
    # Extract the domain from the site object
    site_domain = current_site.domain
    # Define the name of the view we want to generate a URL for
    view_name = "accounts:sessions"
    # Generate the URL for the view using the reverse function
    sessions_url = f"{current_site.protocol}://{site_domain}{reverse(view_name)}"
    # Return the generated URL
    return sessions_url
