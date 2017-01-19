#!/usr/bin/python3
"""Pyxlogin Cisco file."""
import argparse

from pyxlogin import Pyxlogin


class CiscoLogin(Pyxlogin):
    """Pyxlogin Cisco class."""

    PROMPT_USERNAME = r'[uU]sername:\s*$'
    PROMPT_PASSWORD = r'[pP]assword:\s*$'
    PROMPT_ENABLE = r'[-_()\w]+#\s*$'
    PROMPT_LOWAUTH = r'[-_()\w]+>\s*$'
    ENABLE_COMMAND = 'enable'
    INNIT_COMMANDS = [
        'terminal length 0',
        'terminal exec prompt timestamp'
    ]
    EXIT_COMMAND = 'exit'
    LINESEP = '\n'
    AUTO_ENABLE = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Telnet/SSH Cisco routers and execute commands',
        prog='cisco_login.py',
        usage='%(prog)s -u <USERNAME> -p <VTY PASSWORD> -e <ENABLE PASSWORD> <HOSTNAME>',
    )
    parser.add_argument('hostname', help='hostname or IP address', metavar='<HOSTNAME>')
    parser.add_argument('-u', '--username', help='VTY username', metavar='<USERNAME>')
    parser.add_argument('-v', '--password', help='VTY password', metavar='<VTY PASSWORD>')
    parser.add_argument('-w', '--enable_username', help='enable mode username', metavar='<ENABLE USERNAME>')
    parser.add_argument('-e', '--enable_password', help='enable mode password', metavar='<ENABLE PASSWORD>')
    parser.add_argument('-t', '--timeout', help='timeout [sec]', metavar='<TIMEOUT>', default=10, type=int)
    parser.add_argument('-c', '--commands', help='commands to run', metavar='<COMMAND>', nargs='+')
    parser.add_argument('-E', '--encoding', help='remote host encoding (default: utf-8)', metavar='<ENCODING>', default='utf-8')
    parser.add_argument('-T', '--use_telnet', help='use telnet (default is SSH)', action='store_true')
    parser.add_argument('-p', '--port', help='port number', type=int)
    args = parser.parse_args()

    pl = CiscoLogin(
        args.hostname,
        port=args.port,
        username=args.username,
        password=args.password,
        enable_username=args.enable_username,
        enable_password=args.enable_password,
        timeout=args.timeout,
        encoding=args.encoding,
        use_telnet=args.use_telnet,
    )
    try:
        pl.login()
        for command in args.commands:
            print(pl.execute(command))
    except ValueError as e:
        print('ERROR! {}'.format(e))
        print(pl.get_vty_log())
