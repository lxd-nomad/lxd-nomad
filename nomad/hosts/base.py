"""
    Base host
    =========
    This module provides the `Host` base class that is used to define the host OS or distributions
    supported by LXD-Nomad.
"""

import os
import platform
from pathlib import Path

from ..utils.metaclass import with_metaclass

__all__ = ['Host', ]


class _HostBase(type):
    """ Metaclass for all LXD hosts.

    This metaclass ensures that all defined `Host` subclasses have the required attributes and
    proceeds to some validation checks. Additionally it implements the "plugin mount" paradigm and
    stores a list of `Host` subclasses in the namespace of the "plugin mount" class (`host`).
    """

    def __new__(cls, name, bases, attrs):
        super_new = super(_HostBase, cls).__new__
        parents = [base for base in bases if isinstance(base, _HostBase)]

        # We stop here if we are considering the top-level class to which this metaclass was applied
        # and not one of its subclasses (eg. Host).
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Constructs the Host class.
        new_host = super_new(cls, name, bases, attrs)

        # Performs some validation checks.
        # TODO: some validation rules should be implemented here. Not required now while there is no
        # plugin system built in nomad.

        return new_host

    def __init__(cls, name, bases, attrs):
        # We implement the "mount point" paradigm here in order to make all `Host` subclassses
        # available in a single attribute.
        if not hasattr(cls, 'hosts'):
            # The class has no hosts list: this means that we are considering the "plugin mount"
            # class. So we created the list that will hold all the defined `Host` subclasses.
            cls.hosts = []
        else:
            # The `hosts` attribute already exists so we are considering a `Host` subclass, which
            # needs to be registered.
            cls.hosts.append(cls)


class Host(with_metaclass(_HostBase)):
    """ Represents a single host.

    `Host` subclasses will be used by `Container` instances to perform common operations on the
    host side. For example they can be used to retrieve some date (SSH pukeys, ...) or to set up
    contaianers' hosts in the /etc/hosts file. `Host` subclasses should correspond to specific OSes
    or distributions that can be used to run LXD and LXD-Nomad.
    """

    # The `name` of a host is a required attribute and should always be set on `Host` subclasses.
    name = None

    @classmethod
    def detect(cls, lxd_container):
        """ Detects if the host is an "instance" of the considered OS/distribution. """
        return cls.name.lower() in platform.platform()

    def get_ssh_pubkey(self):
        """ Returns the SSH public key of the current user or None if it cannot be found. """
        pubkey_path = Path(os.path.expanduser('~/.ssh/id_rsa.pub'))
        try:
            return pubkey_path.open().read()
        except FileNotFoundError:
            pass
