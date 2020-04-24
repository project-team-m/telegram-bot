from config import TG_TOKEN, proxies
from log.loging import Log
from time import sleep
import requests

def send_message_chat(message):
    run = True
    while run:
        try:
            params = {
                'chat_id': '-230220852',
                'text': message
            }

            r = requests.get('https://api.telegram.org/bot802251438:AAF8f2Xwgpq71BlMKD2b1LwMD_MuR6F9F4g/sendMessage',
                             proxies=proxies,
                             params=params)

            if r.status_code == 200:
                run = True
                Log().action_log('Ye boy, send')
        except:
            sleep(10)
            Log().error_log('EBANY TOR YPAL')
            run = True