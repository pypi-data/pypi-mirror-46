import re

from mock import patch, MagicMock

from cloudshell.networking.alcatel.runners.alcatel_firmware_runner import AlcatelFirmwareRunner
from tests.networking.alcatel.base_test import BaseAlcatelTestCase, DEFAULT_PROMPT, CliEmulator


class TestLoadFirmware(BaseAlcatelTestCase):

    def _setUp(self, attrs=None):
        super(TestLoadFirmware, self)._setUp(attrs)
        self.runner = AlcatelFirmwareRunner(self.logger, self.cli_handler)

    def setUp(self):
        super(TestLoadFirmware, self).setUp()
        self._setUp()

    @patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
    @patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_load_firmware(self, send_mock, recv_mock):
        ftp = 'ftp://test.url'
        file_name = 'both.tim'
        file_system = 'cf1:\\'

        emu = CliEmulator([
            ['^show system information$',
             '{0} show system information\n\n'
             '===============================================================================\n'
             'System Information\n'
             '===============================================================================\n'
             'System Name            : test\n'
             'System Type            : 7210 SAS-M-1\n'
             'System Version         : B-8.0.R4\n\n'
             'BOF Source             : cf1:\n'
             'Image Source           : primary\n'
             'Config Source          : primary\n'
             'Last Booted Config File: cf1:\\config.cfg\n'
             '{0}'''.format(DEFAULT_PROMPT), 1],
            [r'^file copy {0}/{1} {2}{1}$'.format(
                *map(re.escape, (ftp, file_name, file_system))),
                'Copying file cf1:\\config.cfg ... OK\n1 file copied.\n{}'.format(DEFAULT_PROMPT),
                1],
            [r'^bof primary-image {}{}$'.format(*map(re.escape, (file_system, file_name))),
             '{}'.format(DEFAULT_PROMPT),
             1],
            [r'^bof save$',
             'Writing BOF to cf1:/bof.cfg ... OK\nCompleted.\n{}'.format(DEFAULT_PROMPT),
             1],
            [r'^admin reboot upgrade now$',
             [Exception(),
              '{}'.format(DEFAULT_PROMPT)],
             2],  # it called one time, but next time doesn't called send_line command
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        path = '{}/{}'.format(ftp, file_name)
        self.runner.load_firmware(path)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
    @patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_load_firmware_to_cf3(self, send_mock, recv_mock):
        ftp = 'ftp://test.url'
        file_name = 'both.tim'
        file_system = 'cf3:\\'

        emu = CliEmulator([
            ['^show system information$',
             '{0} show system information\n\n'
             '===============================================================================\n'
             'System Information\n'
             '===============================================================================\n'
             'System Name            : test\n'
             'System Type            : 7210 SAS-M-1\n'
             'System Version         : B-8.0.R4\n\n'
             'BOF Source             : cf3:\n'
             'Image Source           : primary\n'
             'Config Source          : primary\n'
             'Last Booted Config File: cf3:\\config.cfg\n'
             '{0}'''.format(DEFAULT_PROMPT), 1],
            [r'^file copy {0}/{1} {2}{1}$'.format(
                *map(re.escape, (ftp, file_name, file_system))),
                'Copying file cf3:\\config.cfg ... OK\n1 file copied.\n{}'.format(DEFAULT_PROMPT),
                1],
            [r'^bof primary-image {}{}$'.format(*map(re.escape, (file_system, file_name))),
             '{}'.format(DEFAULT_PROMPT),
             1],
            [r'^bof save$',
             'Writing BOF to cf3:/bof.cfg ... OK\nCompleted.\n{}'.format(DEFAULT_PROMPT),
             1],
            [r'^admin reboot upgrade now$',
             [Exception(),
              '{}'.format(DEFAULT_PROMPT)],
             2],  # it called one time, but next time doesn't called send_line command
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        path = '{}/{}'.format(ftp, file_name)
        self.runner.load_firmware(path)

        emu.check_calls()
