from .base import Guest


class ArchLinuxGuest(Guest):
    """ This guest can provision ArchLinux containers. """

    name = 'arch'
    barebones_packages = [
        'openssh',
        'python',
    ]

    def install_barebones_packages(self):
        """ Installs packages when the guest is first provisionned. """
        self.run(['pacman', '-S', '--noconfirm'] + self.barebones_packages)

    def set_static_ip_config(self, ip, gateway):
        """ Sets the passed ip & gateway in the current container. """
        network_lines = [
            '[Match]',
            'Name=eth0',
            '',
            '[Network]',
            'Address={}/24'.format(ip),
            'Gateway={}'.format(gateway),
        ]
        self.lxd_container.files.put('/etc/systemd/network/eth0.network', '\n'.join(network_lines))
        self.lxd_container.files.put('/etc/resolv.conf', 'nameserver {}'.format(gateway))
