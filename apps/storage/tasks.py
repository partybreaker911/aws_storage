from celery import shared_task
from django.core.mail import send_mail


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
