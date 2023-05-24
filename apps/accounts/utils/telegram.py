import telegram

"""
    TODO: 
        maybe i will add a function to send a telegram message usesing telegram api library
"""


def send_telegram_message(token, chat_id, message):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)
