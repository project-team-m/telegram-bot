from telegram import Bot
from echo.config import TG_TOKEN, TG_API_URL

def send_message_chat(message):
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL
    )
    bot.send_message(
        chat_id=-1001422975374,
        text=message
    )
