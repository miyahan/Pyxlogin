"""Pyxlogin Smdcn class file."""


class Smdcn(object):
    """Pyxlogin Smdcn class."""

    prompt = r'[-_@()\w]+#\s*$'
    prompt_lowauth = r'[-_@()\w]+$\s*$'
    enable_command = r'enable'
    innit_commands = [
        r'set terminal scroll local off'
    ]
    exit_command = r'exit'
    linesep = '\r\n'
    auto_enable = False
