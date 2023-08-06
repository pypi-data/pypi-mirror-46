import re

from cloudshell.cli.cli_service import CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cloudshell.networking.alcatel.command_templates import configuration


class SystemActions(object):
    def __init__(self, cli_service, logger):
        """System actions

        :param CliService cli_service: enable mode cli_service
        :param logger:
        """

        self._cli_service = cli_service
        self._logger = logger

    def get_startup_config_path(self):
        """Get path to startup file"""

        sys_info = CommandTemplateExecutor(
            self._cli_service,
            configuration.SHOW_SYS_INFO,
        ).execute_command()

        match = re.search(
            r'^\s*Last Booted Config File\s*:\s+(?P<path>.+)$',
            sys_info,
            flags=re.MULTILINE,
        )
        return match.group('path').strip()

    def copy_running_config(self, destination, timeout=120):
        CommandTemplateExecutor(
            self._cli_service,
            configuration.SAVE_RUNNING_CONFIG,
            timeout=timeout,
        ).execute_command(dst=destination)

    def copy(self, src, dst, timeout=120):
        """Copy file from device to ftp or vice versa from ftp to device

        :param src: source path local, ftp or tftp
        :param dst: source path local, ftp or tftp
        :param timeout: session timeout
        """

        CommandTemplateExecutor(
            self._cli_service,
            configuration.COPY,
            timeout=timeout,
        ).execute_command(src=src, dst=dst)

    def copy_additional_settings_files(self, src, dst):
        """Copy additional settings files that can be exists.

        :type src: str
        :type dst: str
        """
        src = re.sub(r'\..{1,3}$', '', src)
        for ext in ('.sdx', '.ndx'):
            try:
                self.copy(src + ext, dst + ext)
            except Exception as e:
                # if we don't have these files just skip
                if 'Copy failed' in str(e):
                    break
                else:
                    raise e

    def change_primary_conf(self, path):
        """Change path to primary config in BOF

        :param path: path to new primary config
        """

        CommandTemplateExecutor(
            self._cli_service,
            configuration.CHANGE_PRIMARY_CONF,
        ).execute_command(path=path)

    def get_primary_config_path(self):
        """Get path to primary config file"""

        bof = CommandTemplateExecutor(
            self._cli_service,
            configuration.SHOW_BOF,
        ).execute_command()

        match = re.search(
            r'^\s*primary-config\s+(?P<path>.+)$',
            bof,
            flags=re.MULTILINE,
        )
        return match.group('path').strip()

    def reboot(self, timeout=3600, upgrade=False):
        """Reboot device"""

        kwargs = {'upgrade': ''} if upgrade else {}
        try:
            CommandTemplateExecutor(
                self._cli_service,
                configuration.REBOOT,
            ).execute_command(**kwargs)
        except Exception:
            self._logger.info('Device rebooted, starting reconnect')
        self._cli_service.reconnect(timeout)

    def change_primary_image(self, folder_path):
        """Change path to primary image in BOF

        :param folder_path: path to new primary image folder
        """

        CommandTemplateExecutor(
            self._cli_service,
            configuration.CHANGE_PRIMARY_IMAGE,
        ).execute_command(folder_path=folder_path)

    def save_bof(self):
        """Save BOF"""

        CommandTemplateExecutor(self._cli_service, configuration.SAVE_BOF).execute_command()

    def get_bof_source(self):
        """Get BOF Source from command 'show system information'.

        Return cf1: cf3:     etc..
        :rtype: str:
        """
        sys_info = CommandTemplateExecutor(
            self._cli_service,
            configuration.SHOW_SYS_INFO,
        ).execute_command()

        # look for the string "BOF Source             : cf1:"
        match = re.search(
            r'^\s*BOF Source\s*:\s+(?P<source>.+)\s*$',
            sys_info,
            flags=re.MULTILINE,
        )
        return match.group('source').strip()
