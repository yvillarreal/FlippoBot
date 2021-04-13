import os

import telegram

global SECRET_TOKEN
global USER_NAME
global CHAT_ID
global URL

ADDRESS = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8443'))
BOT_TOKEN = os.environ.get('SECRET_TOKEN')
BOT_USER_NAME = os.environ.get('USER_NAME')
CHAT = os.environ.get('CHAT_ID')
BOT = telegram.Bot(token=BOT_TOKEN)
URL = os.environ.get('URL')
