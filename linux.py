"""Pyxlogin Linux class file."""


class Linux(object):
    """Pyxlogin Linux class."""

    prompt = r'[-_@~()[\]\s\w]+\$\s*$'
    prompt_lowauth = r'DUMMYDUMMY'
    enable_command = r'DUMMYDUMMY'
    innit_commands = []
    exit_command = r'exit'
    linesep = '\n'
    auto_enable = False
