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
      steps:
        - inline: echo "Hello, World!"

Required options
----------------

steps
=====

The ``steps`` option allows you to define each step to execute when it comes to provision the
considered containers. This option must contain a list of steps corresponding to ``inline`` commands
or corresponding to existing ``scripts``:

.. code-block:: yaml

  name: myproject
  image: ubuntu/xenial

  provisioning:
    - type: shell
      steps:
        - inline: echo "Hello, World!"
        - script: path/to/my/script.sh

Optional options
----------------

side
====

Use the ``side`` option if you want to define that the shell commands/scripts should be executed on
the host side. The default value for this option is ``guest``. Here is an example:

.. code-block:: yaml

  [...]
  provisioning:
    - type: shell
      side: host
      steps:
        - inline: echo "Hello, World!"
