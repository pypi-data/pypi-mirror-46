from .modify_info import _modify_token, _modify_chat_id
from .tprint import tprint
import argparse
from configparser import ConfigParser


def get_arguments():
    parser = argparse.ArgumentParser(prog='notel', description='notel argument')
    parser.add_argument('--set_default_id', '-di', type=str, help='set a default Telegram chat id for notel')
    parser.add_argument('--set_default_token', '-dt', type=str, help='set a default Telegram token for notel')
    parser.add_argument('--chat_id', '-i', type=str, help='set a Telegram chat id to send a message')
    parser.add_argument('--token', '-t', type=str, help='set a Telegram bot token to send a message')
    parser.add_argument('--message', '-m', type=str, help='a message to send to chat id')
    parser.add_argument('--print_console', '-p', type=bool, default=True, help='set notel to print to stdout')

    return parser.parse_args()


def main():
    args = get_arguments()

    if args.set_default_id is not None:
        _modify_chat_id(args.set_default_id)
    if args.set_default_token is not None:
        _modify_token(args.set_default_token)

    if args.set_default_id is None and args.set_default_token is None:
        tprint(args.message, token=args.token,
               chat_id=args.chat_id, print_console=args.print_console)
    


if __name__ == '__main__':
    main()