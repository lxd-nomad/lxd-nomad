import logging

from voluptuous import IsDir, IsFile, Exclusive

from .base import Provisioner


logger = logging.getLogger(__name__)


class AnsibleLocalProvisioner(Provisioner):
    """ Allows to perform provisioning operations using Ansible on the guest. """

    PROVISIONING_DIR = "/provisioning"
    PLAYBOOOK_PATH = "/provisioning/playbook.yml"

    name = "ansible_local"

    schema = {
        Exclusive("playbook", "playbook"): IsFile(),
        Exclusive("dir", "playbook"): IsDir(),
        "ansible_version": str,
    }

    # guest_required_packages_alpine = ['python', ]
    # guest_required_packages_arch = ['python', ]
    # guest_required_packages_centos = ['python', ]
    # guest_required_packages_fedora = ['python2', ]
    # guest_required_packages_gentoo = ['dev-lang/python', ]
    # guest_required_packages_opensuse = ['python3-base', ]
    # guest_required_packages_ol = ['python', ]

    guest_required_packages_debian = ['apt-utils', 'aptitude', 'python', 'python3-pip', 'libssl-dev', ]
    guest_required_packages_ubuntu = ['apt-utils', 'aptitude', 'python', 'python3-pip', 'libssl-dev', ]

    def setup_single(self, guest):
        super().setup_single(guest)

        ansible_version = self.options.get("ansible_version")
        if ansible_version:
            ansible = "ansible=={}".format()
        else:
            ansible = "ansible"

        guest.run(["/usr/bin/pip3", "install", ansible])

    def provision_single(self, guest):
        super().provision_single(guest)

        guest.run(["rm", "-rf", self.PROVISIONING_DIR])
        guest.run(["mkdir", self.PROVISIONING_DIR])

        if self.options.get("playbook"):
            with open(self.homedir_expanded_path(self.options["playbook"])) as fd:
                guest.lxd_container.files.put(self.PLAYBOOOK_PATH, fd.read())

        if self.options.get("dir"):
            guest.lxd_container.files.recursive_put(
                self.homedir_expanded_path(self.options["dir"]),
                self.PROVISIONING_DIR,
            )

        command = [
            "ansible-playbook",
            "--connection=local",
            "--inventory=127.0.0.1,",
            self.PLAYBOOOK_PATH,
        ]

        guest.run(command, quiet=False)
