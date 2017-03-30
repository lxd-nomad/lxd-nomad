import unittest.mock

from lxdock.guests import DebianGuest
from lxdock.hosts import Host
from lxdock.provisioners import ShellProvisioner


class TestShellProvisioner:
    @unittest.mock.patch('subprocess.Popen')
    def test_can_run_commands_on_the_host_side(self, mock_popen):
        host = Host(unittest.mock.Mock())
        guest = DebianGuest(unittest.mock.Mock())
        provisioner = ShellProvisioner(
            './', host, guest, {'commands': ['touch f', ], 'side': 'host', })
        provisioner.provision()
        assert mock_popen.call_args[0] == ('touch f', )

    def test_can_run_commands_on_the_guest_side(self):
        lxd_container = unittest.mock.Mock()
        lxd_container.execute.return_value = ('ok', 'ok', '')
        host = Host(unittest.mock.Mock())
        guest = DebianGuest(lxd_container)
        provisioner = ShellProvisioner(
            './', host, guest, {'commands': ['echo TEST', ], })
        provisioner.provision()
        assert lxd_container.execute.call_count == 1
        assert lxd_container.execute.call_args_list[0][0] == (['echo', 'TEST'], )
