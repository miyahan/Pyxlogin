"""Pyxlogin Alaxala file."""


class Alaxala(object):
    """Pyxlogin Alaxala class."""

    prompt = r'[-_()\w]+#\s*$'
    prompt_lowauth = r'[-_()\w]+>\s*$'
    enable_command = r'enable'
    innit_commands = [
        r'set terminal pager disable',
    ]
    exit_command = r'exit'
    linesep = '\r\n'
    auto_enable = True
