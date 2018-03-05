#!/bin/bash

set -xe

sudo -E apt-get install -y snapd
sudo snap install lxd
sudo snap list

while [ ! -e /var/snap/lxd/common/lxd/unix.socket ]; do
  sleep 0.1
done

sudo lxd --version

sudo lxd init --auto
sudo lxc network create lxdbr0 ipv6.address=none ipv4.address=10.0.3.1/24 ipv4.nat=true
sudo lxc network attach-profile lxdbr0 default eth0

sudo chmod 777 /var/snap/lxd/common/lxd/unix.socket
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -P ""

pip install --upgrade pip setuptools
