import telegram
from configparser import ConfigParser
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(dir_path + '/config.py')
default_token = config['TELEGRAM']['TOKEN'].strip()
default_chat_id = config['TELEGRAM']['CHAT_ID'].strip()


def tprint(msg, token=None, chat_id=None, print_console=True):
    default_bot = telegram.Bot(token = default_token)

    if print_console: 
        print(msg)
    if token == None:
        bot = default_bot
    else:
        bot = telegram.Bot(token = token)
    if chat_id == None:
        chat_id = default_chat_id
    
    bot.send_message(chat_id = chat_id, text=msg)