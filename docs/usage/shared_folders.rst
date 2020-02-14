##############
Shared folders
##############

A common need when using a tool such as LXDock is to make some folders on your system available to
your containers. LXC/LXD provides a feature called "lxc mounts" - LXDock uses it internally in order
to provide support for "shared folders".

You can use the ``shares`` option in order to define which folders should be made available to your
containers. For example:

.. code-block:: yaml

  name: myproject
  image: ubuntu/bionic

  shares:
    - source: /path/to/my/workspace/project/
      dest: /myshare

Of course you can associate many shared folders with your containers. In the previous example, the
content of the ``/path/to/my/workspace/project/`` on the host will be made available to the
container under the ``/myshare`` folder.

The problem with shared folder permissions
------------------------------------------

Shared folders in LXDock use lxc mounts. This is simple and fast, but there are problems with
permissions: shared folders means shared permissions. Changing permissions in the container means
changing them in the host as well, and vice versa. That leaves us with a problem that is tricky to
solve gracefully. Things become more complicated when our workflow has our container create files in
that shared folder. What permissions do we give these files?

There are two possible ways for making a shared folder actually usable on both ends:

* `Posix ACLs <https://www.reddit.com/r/homelab/comments/4h0erv/resolving_permissions_issues_with_host_bind/>`_
* ID mapping

LXDock uses the latter method.

Normally, in an unprivileged container, the user (and group) IDs in the container are mapped to 
high values on the host without any privliges (typically the uid 1000 in the container is mapped to 
165636 on the host). By using the *raw.idmap* configiration setting of LXD, this behaviour can be overridden.


You should note that users created by your provisioning tools (eg. using Ansible) won't be able to
access your shares on the guest side. This is because LXDock has no knowledge of the users who
should have access to your shares. Moreover, your users/groups, when the container is initially
created, don't exist yet! That is why it does nothing. 
You should instead make use of the ``users`` option in order to force LXDock to create some users. 
The first user created this way will have his UID and GID mapped to the host's user and thus have access to the shared folder.


Usage
-----

Use the following *lxdock.yml*:

.. code-block:: yaml

  name: myproject
  image: ubuntu/bionic

  shares:
    - source: /path/to/my/workspace/project/
      dest: /myshare

  users:
    - name: test01
    - name: test02
      home: /opt/test02

Furthermore, you need to add the lines

.. code-block:: txt

  lxd:1000:1
  root:1000:1

to the files */etc/subuid* and */etc/subgid* (assuming the your host user has the UID and GID 1000).
This will make the shared folder read and writable by the user 1000 on the host as well as *test01* in the container.

Caveats
-------

* There is currently no automatic way for two users in the container to share a folder with the host
* The mapping makes all processes in the container by the first user run with the host user's ID, weakening the isolation of the container
