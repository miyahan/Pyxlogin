"""Pyxlogin Cisco file."""


class Cisco(object):
    """Pyxlogin Cisco class."""

    prompt = r'[-_()\w]+#\s*$'
    prompt_lowauth = r'[-_()\w]+>\s*$'
    enable_command = r'enable'
    innit_commands = [
        r'terminal length 0',
        r'terminal exec prompt timestamp'
    ]
    exit_command = r'exit'
    linesep = '\n'
    auto_enable = True
