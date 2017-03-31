"""
    Base provisioner
    ================
    This module provides the `Provisioner` base class that is used to define the provisioners
    supported by LXDock (eg. Ansible, ...).
"""

import os

from ..utils.metaclass import with_metaclass

__all__ = ['Provisioner', ]


class InvalidProvisioner(Exception):
    """ The `Provisioner` subclass is not valid. """


class _ProvisionerBase(type):
    """ Metaclass for all LXDock provisioners.

    This metaclass ensures that all defined `Provisioner` subclasses have the required attributes
    and proceeds to some validation checks. Additionally it implements the "plugin mount" paradigm
    and stores a dictionary of `Provisioner` subclasses in the namespace of the "plugin mount"
    class (`Provisioner`).
    """

    def __new__(cls, name, bases, attrs):
        super_new = super(_ProvisionerBase, cls).__new__
        parents = [base for base in bases if isinstance(base, _ProvisionerBase)]

        # We stop here if we are considering the top-level class to which this metaclass was applied
        # and not one of its subclasses (eg. Provisioner).
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Constructs the Provisioner class.
        new_provisioner = super_new(cls, name, bases, attrs)

        # Performs some validation checks.
        if not new_provisioner.name:
            raise InvalidProvisioner(
                "The 'name' attribute of Provisioner subclasses cannot be None")
        if not new_provisioner.schema:
            raise InvalidProvisioner(
                "The 'schema' attribute of Provisioner subclasses cannot be None")

        return new_provisioner

    def __init__(cls, name, bases, attrs):
        # We implement the "mount point" paradigm here in order to make all `Provisioner`
        # subclassses available in a single attribute.
        if not hasattr(cls, 'provisioners'):
            # The class has no provisioners dict: this means that we are considering the
            # "plugin mount" class. So we created the dict that will hold all the defined
            # `Provisioner` subclasses.
            cls.provisioners = {}
        else:
            # The `provisioners` attribute already exists so we are considering a `Provisioner`
            # subclass, which needs to be registered.
            cls.provisioners.update({cls.name.lower(): cls})


class Provisioner(with_metaclass(_ProvisionerBase)):
    """ Represents a single provisioner.

    `Provisioner` subclasses will be used by `Container` instances to run provisioning operations
    associated with the considered containers. For example they can be used to run Ansible playbooks
    to provision a web application on the container.
    """

    # The `name` of a provisioner is a required attribute and should always be set on `Provisioner`
    # subclasses.
    name = None

    # The `schema` of a provisioner should be a dictionary using voluptuous helpers. This dictionary
    # must define the "local" schema that should be provided in the LXDock file in order to use the
    # considered provisioner.
    schema = None

    def __init__(self, homedir, host, guest, options):
        self.homedir = homedir
        self.host = host
        self.guest = guest
        self.options = options.copy()

    def provision(self):
        """ Performs the provisioning operations using the considered provisioner. """
        # This method should be overriden in `Provisioner` subclasses.

    ##################
    # HELPER METHODS #
    ##################

    def homedir_expanded_path(self, relative_path):
        """ Expands the considered path with the absolute path of the home homedir. """
        return os.path.join(self.homedir, relative_path)
