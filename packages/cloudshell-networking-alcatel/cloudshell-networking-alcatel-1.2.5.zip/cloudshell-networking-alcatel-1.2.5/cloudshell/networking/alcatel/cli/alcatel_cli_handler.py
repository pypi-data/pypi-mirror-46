#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.cli_service_impl import CliServiceImpl
from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.session.telnet_session import TelnetSession
from cloudshell.devices.cli_handler_impl import CliHandlerImpl

from cloudshell.networking.alcatel.cli.alcatel_command_modes import EnableCommandMode, \
    ConfigCommandMode
from cloudshell.networking.alcatel.sessions.console_ssh_session import ConsoleSSHSession
from cloudshell.networking.alcatel.sessions.console_telnet_session import ConsoleTelnetSession


class AlcatelCliHandler(CliHandlerImpl):
    def __init__(self, cli, resource_config, logger, api):
        super(AlcatelCliHandler, self).__init__(cli, resource_config, logger, api)
        self.modes = CommandModeHelper.create_command_mode(resource_config, api)
        self._enable_password = None

    @property
    def default_mode(self):
        return self.modes[EnableCommandMode]

    @property
    def enable_mode(self):
        return self.modes[EnableCommandMode]

    @property
    def config_mode(self):
        return self.modes[ConfigCommandMode]

    def _console_ssh_session(self):
        console_port = int(self.resource_config.console_port)
        session = ConsoleSSHSession(self.resource_config.console_server_ip_address,
                                    self.username,
                                    self.password,
                                    console_port,
                                    self.on_session_start)
        return session

    def _console_telnet_session(self):
        console_port = int(self.resource_config.console_port)
        return [ConsoleTelnetSession(self.resource_config.console_server_ip_address,
                                     self.username,
                                     self.password,
                                     console_port,
                                     self.on_session_start),
                ConsoleTelnetSession(self.resource_config.console_server_ip_address,
                                     self.username,
                                     self.password,
                                     console_port,
                                     self.on_session_start,
                                     start_with_new_line=True)
                ]

    def _new_sessions(self):
        if self.cli_type.lower() == SSHSession.SESSION_TYPE.lower():
            new_sessions = self._ssh_session()
        elif self.cli_type.lower() == TelnetSession.SESSION_TYPE.lower():
            new_sessions = self._telnet_session()
        elif self.cli_type.lower() == "console":
            new_sessions = list()
            new_sessions.append(self._console_ssh_session())
            new_sessions.extend(self._console_telnet_session())
        else:
            new_sessions = [self._ssh_session(), self._telnet_session(),
                            self._console_ssh_session()]
            new_sessions.extend(self._console_telnet_session())
        return new_sessions

    @property
    def enable_password(self):
        if not self._enable_password:
            password = self.resource_config.enable_password
            self._enable_password = self._api.DecryptPassword(password).Value
        return self._enable_password

    def on_session_start(self, session, logger):
        """Send default commands to configure/clear session outputs"""

        cli_service = CliServiceImpl(session, self.enable_mode, logger)
        cli_service.send_command('enable-admin', action_map={
            r'Password': lambda session, logger: session.send_line(self.enable_password, logger),
        })
        cli_service.send_command('environment no more')
