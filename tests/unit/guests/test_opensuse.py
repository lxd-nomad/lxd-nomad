import unittest.mock

from lxdock.guests import OpenSUSEGuest


class TestOpenSUSEGuest:
    def test_can_install_barebones_packages(self):
        lxd_container = unittest.mock.Mock()
        lxd_container.execute.return_value = ('ok', 'ok', '')
        guest = OpenSUSEGuest(lxd_container)
        guest.install_ansible_packages()
        assert lxd_container.execute.call_count == 1
        assert lxd_container.execute.call_args[0] == \
            (['zypper', '--non-interactive', 'install'] +
             OpenSUSEGuest.ansible_packages, )
