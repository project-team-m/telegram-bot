import telebot
from telebot import apihelper
from config import TG_TOKEN, proxy
from time import sleep
apihelper.proxy = {'https': proxy}

def send_message_chat(message):
    try:
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_message(-230220852, message)
    except:
        sleep(1)
        send_message_chat(message)