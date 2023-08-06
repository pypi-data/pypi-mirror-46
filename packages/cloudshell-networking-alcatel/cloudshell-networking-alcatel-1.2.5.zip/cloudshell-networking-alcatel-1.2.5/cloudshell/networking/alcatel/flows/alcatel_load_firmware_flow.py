from cloudshell.devices.flows.action_flows import LoadFirmwareFlow
from cloudshell.devices.networking_utils import UrlParser

from cloudshell.networking.alcatel.command_actions.system_actions import SystemActions


class AlcatelLoadFirmwareFlow(LoadFirmwareFlow):
    def execute_flow(self, path, vrf, timeout):
        """Load a firmware onto the device.

        :param path: The path to the firmware file, including the firmware file name
        :param vrf: Virtual Routing and Forwarding Name
        :param timeout:
        """
        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            system_action = SystemActions(enable_session, self._logger)
            bof_source = system_action.get_bof_source()
            dst = self._get_dst_path(bof_source, path)
            system_action.copy(path, dst)
            system_action.change_primary_image(dst)
            system_action.save_bof()
            system_action.reboot(upgrade=True)

    @staticmethod
    def _get_dst_path(bof_source, path):
        """Create file path on the remote resource.

        :param str bof_source: "cf1:", "cf3:" etc
        :param str path: ftp://ftp_host/file_name, etc
        """
        file_name = UrlParser.parse_url(path)[UrlParser.FILENAME]
        return '{}\\{}'.format(bof_source, file_name)
