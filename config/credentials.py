import os

import telegram

global SECRET_TOKEN
global USER_NAME
global CHAT_ID
global URL

# ADDRESS = '0.0.0.0'
# PORT = int(os.environ.get('PORT', '8443'))
# BOT_TOKEN = os.environ.get('SECRET_TOKEN')
# BOT_USER_NAME = os.environ.get('USER_NAME')
# CHAT = os.environ.get('CHAT_ID')
# BOT = telegram.Bot(token=BOT_TOKEN)
# URL = os.environ.get('URL')

ADDRESS = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8443'))
BOT_TOKEN = '1666206664:AAHl7Aa0TPBXLJ8fWFEKrPL10gRJ5k2RNvk'
BOT_USER_NAME = '@flippo_father_bot'
CHAT = '146321299'
BOT = telegram.Bot(BOT_TOKEN)
URL = 'https://flipo-app.herokuapp.com/'
