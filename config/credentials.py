import os

import telegram

global SECRET_TOKEN
global USER_NAME
global CHAT_ID
global URL

ADDRESS = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8443'))
BOT_TOKEN = SECRET_TOKEN
BOT_USER_NAME = USER_NAME
CHAT = CHAT_ID
BOT = telegram.Bot(token=BOT_TOKEN)
URL = URL
