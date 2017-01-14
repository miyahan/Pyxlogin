"""Pyxlogin Smdcf class file."""


class Smdcf(object):
    """Pyxlogin Smdcf class."""

    prompt = r'[-_@()\w]+#\s*$'
    prompt_lowauth = r'[-_@()\w]>\s*$'
    enable_command = r'enable'
    innit_commands = [
        r'more-function disable'
    ]
    exit_command = r'logout'
    linesep = '\r\n'
    auto_enable = False
