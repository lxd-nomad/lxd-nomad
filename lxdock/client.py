import os

import pylxd
from pkg_resources import parse_version as ver


def get_client():
    """ Returns a PyLXD client to be used to orchestrate containers. """
    # Fixed a bug upstream: https://github.com/lxc/pylxd/issues/257
    lxd_dir_not_set = "LXD_DIR" not in os.environ
    snap_socket_exists = os.path.exists('/var/snap/lxd/common/lxd/unix.socket')
    insufficient_version = ver(pylxd.__version__) < ver("2.2.5")

    if lxd_dir_not_set and snap_socket_exists and insufficient_version:
        os.environ["LXD_DIR"] = "/var/snap/lxd/common/lxd"

    return pylxd.Client()
