from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from apps.storage.models import File
from apps.storage.utils.archivation import Archivation

"""
    TODO: Implement using template for email
"""


@shared_task
def send_file_share_email(file_url: str, recipient_email: str) -> None:
    """
    Sends an email with a shared file URL to a recipient.

    Args:
        file_url (str): The URL to the shared file.
        recipient_email (str): The email address of the recipient.

    Returns:
        None
    """
    subject = "File Sharing Notification"
    message = f"You have been granted access to a shared file. You can access it at: {file_url}"
    sender = "your_email@example.com"
    try:
        send_mail(subject, message, sender, [recipient_email])
    except Exception as e:
        print(e)


@shared_task
def create_archive(file_id):
    """
    Given a file ID, creates a zip archive of the file and returns the path to the archive.

    Args:
        file_id (int): The ID of the file to be archived.

    Returns:
        str: The path to the created archive file, or None if the file does not exist or the user does not have permission to download it.
    """
    try:
        file_obj = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return None

    # Check if the user has permission to download the file
    if not file_obj.user == request.user:
        return None

    # Get the path to the file
    file_path = file_obj.file.path

    # Create the archive path
    archive_path = settings.MEDIA_ROOT / "archives"
    archive_path.mkdir(parents=True, exist_ok=True)
    archive_file = archive_path / f"{file_obj.name}.zip"

    # Create an instance of the Archivation utility
    archiver = Archivation()

    # Create the archive using the Archivation utility
    archiver.create_archive(file_path, archive_file)

    return str(archive_file)
