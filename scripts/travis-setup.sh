#!/bin/bash

set -xe

sudo -E apt-get purge lxd lxd-client
sudo -E apt-get install -y snapd
sudo snap install lxd
sudo snap list

export PATH="/snap/bin:$PATH"
sudo sh -c 'echo PATH=/snap/bin:$PATH >> /etc/environment'

# lxd waitready
while [ ! -S /var/snap/lxd/common/lxd/unix.socket ]; do
  sleep 0.5
done
sudo usermod -a -G lxd travis

sudo lxd --version

sudo lxd init --auto
sudo lxc network create lxdbr0 ipv6.address=none ipv4.address=10.0.3.1/24 ipv4.nat=true
sudo lxc network attach-profile lxdbr0 default eth0


