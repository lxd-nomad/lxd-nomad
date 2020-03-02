Getting started
===============

Requirements
------------

* `Python`_ 3.5+
* `LXD`_ 2.0+
* any provisioning tool you wish to use with LXDock

.. _Python: https://www.python.org
.. _LXD: https://linuxcontainers.org/lxd/

Building LXDock on Linux
------------------------

LXDock should build very easily on Linux provided you have LXD available on your system.

Prerequisite: install LXD
~~~~~~~~~~~~~~~~~~~~~~~~~

You may want to skip this section if you already have a working installation
of LXD on your system.

The official install method for LXD is via Snap which works on Ubuntu 14.04 and
higher and is also available for `other distributions <https://snapcraft.io/docs/installing-snapd>`__.
To install LXD from a Snap in Ubuntu:

.. code-block:: console

  $ sudo apt-get install snapd
  $ sudo snap install lxd
  $ sudo snap start lxd

.. note::

  If you have already installed and configured LXD from apt earlier and
  want to upgrade to the Snap version, you may need to purge LXD packages
  first and reboot for the old network bridge to be removed. You can migrate
  existing containers using ``lxd.migrate`` or just start fresh.

  .. code-block:: console

    $ sudo apt-get purge lxd lxd-client


In older versions of Ubuntu (16.04 - 18.04) LXD is also available in the
standard repository:

.. code-block:: console

  $ sudo apt-get install lxd

For Fedora, LXD is also available through an experimental COPR repository.
Unfortunately SELinux is not yet supported, therefore make sure it is
disabled or set to permissive. Then run:

.. code-block:: console

  $ dnf copr enable ganto/lxd
  $ dnf install lxd lxd-tools

You should now be able to configure your LXD installation using:

.. code-block:: console

  $ newgrp lxd  # ensure your current user can use LXD
  $ sudo lxd init

.. note::

  The ``lxd init`` command will ask you to choose the settings to apply to your LXD installation in
  an interactive way (storage backend, network configuration, etc). But if you just want to go fast
  you can try the following commands (note that this will only work for **LXD 2.3+**):

  .. code-block:: console

    $ newgrp lxd
    $ sudo lxd init --auto
    $ lxc network create lxdbr0 ipv6.address=none ipv4.address=10.0.3.1/24 ipv4.nat=true
    $ lxc network attach-profile lxdbr0 default eth0

You can now check if your LXD installation is working using:

  .. code-block:: console

    $ lxc launch ubuntu: first-machine && lxc exec first-machine bash

.. note::

  You can use ``lxc stop first-machine`` to stop the previously created container.

Prepare host for shared folders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LXDock uses ``raw.idmap`` for shared folders to so that files on the share
that are owned by the host user appear to be owned by the container user
inside the container, even if new files are created inside the container.

To use shares, the following needs to be run once to prepare the host,
then LXD needs to be restarted.

.. code-block:: console

  $ printf "lxd:$(id -u):1\nroot:$(id -u):1\n" | sudo tee -a /etc/subuid
  $ printf "lxd:$(id -g):1\nroot:$(id -g):1\n" | sudo tee -a /etc/subgid

To restart LXD use ``sudo snap restart lxd`` or ``sudo service restart lxd``
or equivalent for your system.

Install LXDock via pip
~~~~~~~~~~~~~~~~~~~~~~

You should now be able to install LXDock using:

.. code-block:: console

  $ pip3 install lxdock

.. note::

  It is good practice to install lxdock in a virtualenv rather than installing
  it globally as root, but make sure you always use a python3 virtualenv.
  To use lxdock from any location without having to activate this virtualenv,
  you can create a symlink from the lxdock executable in the virtualenv to
  ``/usr/bin/lxdock`` or ``/usr/local/bin/lxdock``.

.. note::

  Don't have ``pip3`` installed on your system? Most distros have a specific package for it, it's
  only a matter of installing it. For example, on Debian and Ubuntu, it's ``python3-pip``.
  Otherwise, `Stackoverflow can help you <http://stackoverflow.com/a/6587528>`__.

Install LXDock via snap
~~~~~~~~~~~~~~~~~~~~~~~

In order to build the snap package under Ubuntu, you need to install the
`snapcraft` package first. You can then build by running

.. code-block:: console

  $ make snap

The package file is then created in the local directory and you can install it
with

.. code-block:: console

  $ sudo snap install lxdock_VERSION_amd64.snap --dangerous

The `dangerous` flag is necessary, because you are installing a local package
instead of a signed one downloaded from the official snap store.

The executable can be found at ``/snap/bin/lxdock``. You might need to re-login
or manually update your PATH environment variable.

.. note::

  Using lxdock from a snap package only works, if LXD itself is also installed via snap.

  If you manually build the snap using ``snapcraft``, you should delete the directories
  ``parts``, ``stage``, ``prime`` and ``snap`` afterwards, as they might interfere with the tests.

Command line completion
-----------------------

LXDock can provide completion for commands, options and container names.

Bash
~~~~

If you use Bash, you have to make sure that bash completion is installed (which should be the case
for most Linux installations). In order to get completion for LXDock, you should place the
``contrib/completion/bash/lxdock`` file at ``/etc/bash.completion.d/lxdock`` (or at any other place
where your distribution keeps completion files):

.. code-block:: console

  $ sudo curl -L https://raw.githubusercontent.com/lxdock/lxdock/$(lxdock --version | cut -d ' ' -f 2)/contrib/completion/bash/lxdock -o /etc/bash_completion.d/lxdock

Make sure to restart your shell before trying to use LXDock's bash completion.

ZSH
~~~

To add zsh completion for LXDock, place the ``contrib/completion/zsh/_lxdock`` file at
``/usr/share/zsh/vendor-completions/_lxdock`` (or another folder in ``$fpath``):

.. code-block:: console

  $ sudo curl -L https://raw.githubusercontent.com/lxdock/lxdock/$(lxdock --version | cut -d ' ' -f 2)/contrib/completion/zsh/_lxdock -o /usr/share/zsh/vendor-completions/_lxdock

Make sure to restart your shell before trying to use LXDock's zsh completion.

Your first LXDock file
----------------------

Create a file called ``.lxdock.yml`` (or ``lxdock.yml``) in your project directory and paste the
following:

.. code-block:: yaml

  name: myproject

  containers:
    - name: test01
      image: ubuntu/bionic

    - name: test02
      image: archlinux

This LXDock file defines a project (``myproject``) and two containers, ``test01`` and ``test02``.
These containers will be constructed using respectively the ``ubuntu/bionic`` and the ``archlinux``
images (which will be pulled from an image server - https://images.linuxcontainers.org by default).

Now from your project directory, start up your containers using the following command:

.. code-block:: console

  $ lxdock up
  Bringing container "test01" up
  Bringing container "test02" up
  ==> test01: Unable to find container "test01" for directory "[PATH_TO_YOUR_PROJECT]"
  ==> test01: Creating new container "myproject-test01-11943450" from image ubuntu/bionic
  ==> test01: Starting container "test01"...
  ==> test01: No IP yet, waiting 10 seconds...
  ==> test01: Container "test01" is up! IP: [CONTAINER_IP]
  ==> test01: Doing bare bone setup on the machine...
  ==> test01: Adding ssh-rsa [SSH_KEY] to machine's authorized keys
  ==> test01: Provisioning container "test01"...
  ==> test02: Unable to find container "test02" for directory "[PATH_TO_YOUR_PROJECT]"
  ==> test02: Creating new container "myproject-test02-11943450" from image archlinux
  ==> test02: Starting container "test02"...
  ==> test02: No IP yet, waiting 10 seconds...
  ==> test02: Container "test02" is up! IP: [CONTAINER_IP]
  ==> test02: Doing bare bone setup on the machine...
  ==> test02: Adding ssh-rsa [SSH_KEY] to machine's authorized keys
  ==> test02: Provisioning container "test02"...

*Congrats! You're in!*

Problems?
---------

If you're having problems trying to run your container, try running them in :ref:`conf-privileged`
mode. Many older distributions have an init system that doesn't work well with unprivileged
containers (`debian/jessie` notably). Some host-side problems can also be worked around by running
privileged containers.


If you received a permission denied error running the lxc network commands below:

.. code-block:: console

    $ lxc network create lxdbr0 ipv6.address=none ipv4.address=10.0.3.1/24 ipv4.nat=true
    $ lxc network attach-profile lxdbr0 default eth0

Run these commands below and then run the lxc network commands again. You should now be able
to proceed with the remaining instructions.

.. code-block:: console

    $ sudo systemctl stop lxd.socket
    $ sudo systemctl start lxd.socket
