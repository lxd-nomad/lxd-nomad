from .base import Guest


class DebianGuest(Guest):
    """ This guest can provision Debian containers. """

    name = 'debian'
    barebones_packages = [
        'apt-utils',
        'aptitude',
        'openssh-server',
        'python',
    ]

    def install_barebones_packages(self):
        """ Installs packages when the guest is first provisionned. """
        self.run(['apt-get', 'install', '-y'] + self.barebones_packages)

    def set_static_ip_config(self, ip, gateway):
        """ Sets the passed ip & gateway in the current container. """
        iface_lines = [
            'auto lo',
            'iface lo inet loopback',
            'auto eth0',
            'iface eth0 inet static',
            '\taddress {}'.format(ip),
            '\tnetmask 255.255.255.0',
            '\tgateway {}'.format(gateway),
        ]
        self.lxd_container.files.put('/etc/network/interfaces', '\n'.join(iface_lines))
        self.lxd_container.files.put('/etc/resolv.conf', 'nameserver {}'.format(gateway))
