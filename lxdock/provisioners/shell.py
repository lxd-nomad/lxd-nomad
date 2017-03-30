from voluptuous import Any, Required

from .base import Provisioner


class ShellProvisioner(Provisioner):
    """ Allows to perform provisioning shell operations on the host/guest sides. """

    name = 'shell'
    schema = {
        Required('commands'): [str, ],
        'side': Any('guest', 'host'),
    }

    def provision(self):
        """ Executes the shell commands in the guest container or in the host. """
        host_or_guest = getattr(self, self._side)
        [host_or_guest.run(command.split()) for command in self.options['commands']]

    @property
    def _side(self):
        return self.options.get('side', 'guest')
