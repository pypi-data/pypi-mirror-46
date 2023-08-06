#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_mode import CommandMode


# do not include symbol \n from previous line
NEW_LINE_OR_BEGIN_LINE = r'((?<=\n)|^)'


class EnableCommandMode(CommandMode):
    PROMPT = r'{}\*?[^>\n]+?#\s*$'.format(NEW_LINE_OR_BEGIN_LINE)
    ENTER_COMMAND = ''
    EXIT_COMMAND = ''

    def __init__(self, resource_config, api):
        """Initialize Enable command mode - default command mode for Alcatel Shells"""

        self.resource_config = resource_config
        self._api = api
        CommandMode.__init__(self, self.PROMPT, self.ENTER_COMMAND, self.EXIT_COMMAND)


class ConfigCommandMode(CommandMode):
    PROMPT = r'{}\*?[^>\n]+?>config#\s*$'.format(NEW_LINE_OR_BEGIN_LINE)
    ENTER_COMMAND = 'configure'
    EXIT_COMMAND = 'exit'

    def __init__(self, resource_config, api):
        """Initialize Config command mode"""

        self.resource_config = resource_config
        self._api = api
        CommandMode.__init__(self, self.PROMPT, self.ENTER_COMMAND, self.EXIT_COMMAND)


CommandMode.RELATIONS_DICT = {
    EnableCommandMode: {
        ConfigCommandMode: {},
    }
}
