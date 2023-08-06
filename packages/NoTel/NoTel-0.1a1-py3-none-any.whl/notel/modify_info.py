from configparser import ConfigParser
import os


def _modify_chat_id(chat_id):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser()
    config.read(dir_path + '/config.py')

    config.set('TELEGRAM', 'CHAT_ID', chat_id)
    
    with open(dir_path + '/config.py', 'w') as configfile:
        config.write(configfile)


def _modify_token(token):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser()
    config.read(dir_path + '/config.py')

    config.set('TELEGRAM', 'TOKEN', token)
    
    with open(dir_path + '/config.py', 'w') as configfile:
        config.write(configfile)


def _read_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + '/config.py', 'r') as configfile:
        print(configfile.readlines())