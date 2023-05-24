import requests

from django.conf import settings

from celery import shared_task


@shared_task
def send_telegram_message_task(chat_id: int, message: str) -> bool:
    """
    Sends a message to a specified chat ID using the Telegram bot API.

    Args:
        chat_id (int): The ID of the chat to send the message to.
        message (str): The message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    # Get Telegram bot token from settings
    telegram_token = settings.TELEGRAM_BOT_TOKEN
    # Construct URL for sending message
    telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    # Create payload with chat ID and message text
    payload = {"chat_id": chat_id, "text": message}
    # Create payload with chat ID and message text
    response = requests.post(telegram_url, data=payload)
    # Return True if request was successful, False otherwise
    if response.status_code == 200:
        return True
    else:
        return False
