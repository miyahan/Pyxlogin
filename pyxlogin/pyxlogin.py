"""Pyxlogin class file."""
import io
import logging

import pexpect


class Pyxlogin(object):
    """Pyxlogin class."""

    def __init__(
        self,
        hostname,
        port=None,
        username='',
        password='',
        enable_username=None,
        enable_password=None,
        timeout=10,
        use_telnet=False,
        encoding='utf-8',
    ):
        """constructor.

        :param str hostname: remote host hostname
        :param int port: remote host port (default:auto)
        :param str username: remote host username
        :param str password: remote host password
        :param str enable_username: remote host enable-mode username (If blank, use username value)
        :param str enable_password: remote host enable-mode password (If blank, use password value)
        :param int timeout: pexpect spawn timeout [sec]
        :param boolean use_telnet: if True, connect by telnet (default: False (SSH))
        :param str encoding: remote host charcode (default: utf-8)
        """
        self.logger = logging.getLogger('pyxlogin')
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(logging.Formatter('[%(name)s] %(asctime)s %(levelname)s %(message)s'))
        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(logging.DEBUG)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.enable_username = enable_username or username or ''
        self.enable_password = enable_password or password or ''
        self.timeout = int(timeout)
        self.encoding = encoding

        if port is int and 0 < port < 65536:
            self.port = port
        elif use_telnet:
            self.port = 23
        else:
            self.port = 22

        if use_telnet:
            self.protocol = 'telnet'
            self.spawn_command = 'telnet "{}" {}'.format(self.hostname, self.port)
        else:
            self.protocol = 'ssh'
            self.spawn_command = 'ssh "{}@{}" -p {}'.format(self.username, self.hostname, self.port)

        self.log_mixed = io.StringIO()
        self.log_read = io.StringIO()
        self.log_send = io.StringIO()

    def login(self):
        """login to remote host."""
        self.logger.debug("Start pexpect.spawnu('{}')".format(self.spawn_command))
        self.exp = pexpect.spawnu(
            self.spawn_command,
            encoding=self.encoding,
            logfile=self.log_mixed,
            timeout=self.timeout,
        )
        self.exp.logfile_read = self.log_read
        self.exp.logfile_send = self.log_send
        while True:
            index = self.exp.expect([
                self.PROMPT_ENABLE,  # 0
                self.PROMPT_LOWAUTH,  # 1
                self.PROMPT_USERNAME,  # 2
                self.PROMPT_PASSWORD,  # 3
                r'Are you sure you want to continue connecting',  # 4
                r'Host key verification failed',  # 5
                r'Authentication failed',  # 6
                r'Access denied',  # 7
                r'Connection refused',  # 8
                r'(Connection closed by|Connection to \[^\n\r]+ closed)',  # 9
                r'Host is unreachable',  # 10
                r'No address associated with',  # 11
            ])
            if index == 0:
                self.logger.debug('login: prompt was detected. login succeeded.')
                break
            elif index == 1:
                if self.AUTO_ENABLE:
                    self.logger.debug('login: low-authority prompt was detected. will call enable().')
                    self.enable()
                else:
                    self.logger.debug('login: low-authority prompt was detected. login succeeded.')
                    break
            elif index == 2:
                self.logger.debug('login: username prompt was detected. will send username.')
                self.exp.send(self.username + self.LINESEP)
            elif index == 3:
                self.logger.debug('login: password prompt was detected. will send password.')
                self.exp.send(self.password + self.LINESEP)
            elif index == 4:
                self.logger.debug('login: Host key verification message was detected. will answer YES.')
                self.exp.send('yes' + self.LINESEP)
            elif index == 5:
                self.logger.debug('login: Host key verification failed')
                raise Exception('Host key verification failed')
            elif index == 6:
                self.logger.debug('login: Authentication failed')
                raise Exception('Authentication failed')
            elif index == 7:
                self.logger.debug('login: Access denied.')
                raise Exception('Access denied')
            elif index == 8:
                self.logger.debug('login: Connection refused')
                raise Exception('Connection refused')
            elif index == 9:
                self.logger.debug('login: Connection closed')
                raise Exception('Connection closed')
            elif index == 10:
                self.logger.debug('login: Host is unreachable')
                raise Exception('Host is unreachable')
            elif index == 11:
                self.logger.debug('login: No address associated')
                raise Exception('No address associated')

        for command in self.INNIT_COMMANDS:
            self.logger.debug("login: Execute innit command: '{}'".format(command))
            self.execute(command)

    def enable(self):
        """change to enable/root mode."""
        self.exp.send(self.ENABLE_COMMAND + self.LINESEP)
        while True:
            index = self.exp.expect([
                self.PROMPT_ENABLE,  # 0
                self.PROMPT_USERNAME,  # 1
                self.PROMPT_PASSWORD,  # 2
                r'Access denied',
            ])
            if index == 0:
                self.logger.debug('enbale: enable-prompt was detected. enable succeeded.')
                self.exp.send(self.LINESEP)
                break
            elif index == 1:
                self.logger.debug('enable: username prompt was detected. will send enable-username.')
                self.exp.send(self.enable_username + self.LINESEP)
            elif index == 2:
                self.logger.debug('enable: password prompt was detected. will send enable-password.')
                self.exp.send(self.enable_password + self.LINESEP)
            elif index == 3:
                self.logger.debug('enable: enable failed.')
                raise Exception('Enable failed')

    def execute(self, command, expect=[], newline=True, timeout=None):
        """execute command on remote host."""
        expect.append(self.PROMPT_ENABLE)
        expect.append(self.PROMPT_LOWAUTH)
        timeout = timeout or self.timeout
        if newline:
            self.exp.send(command + self.LINESEP)
        else:
            self.exp.send(command)

        self.exp.expect(expect, timeout=timeout)
        return self.exp.before

    def get_vty_log(self, type='mixed'):
        """get all VTY log.

        :param str type:
            mixed: mixed read/send log (default)
            read: read log (server -> client) only
            send: send log (client -> server) only
        """
        if type == 'mixed':
            return self.log_mixed.getvalue()
        elif type == 'read':
            return self.log_read.getvalue()
        elif type == 'send':
            return self.log_send.getvalue()
        else:
            raise ValueError('log type is invalid')
