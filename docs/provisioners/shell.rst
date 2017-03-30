#####
Shell
#####

The shell provisioner allows you to execute commands on the guest side or the host side in order to
provision your containers.

Usage
-----

Just append a ``shell`` provisioning operation to your LXDock file as follows:

.. code-block:: yaml

  name: myproject
  image: ubuntu/xenial

  provisioning:
    - type: shell
      commands:
        - echo "Hello, World!"

Required options
----------------

commands
========

The ``commands`` option allows you to define which commands should be executed on the guest side or
the host side. It should contain a list of commands.

Optional options
----------------

side
====

Use the ``side`` option if you want to define that the shell commands should be executed on the
host side. The default value for this option is ``guest``. Here is an example:

.. code-block:: yaml

  [...]
  provisioning:
    - type: shell
      side: host
      commands:
        - echo "TEST"
