#!/usr/bin/env bash
# install inspec
apt update

# install inspec
apt install -y --no-install-recommends ruby
curl https://omnitruck.chef.io/install.sh | sudo bash -s -- -P inspec

# install tuptime for detailed uptime
cd /tmp
git clone https://github.com/rfrail3/tuptime.git
cd tuptime
bash tuptime-install.sh

apt install -y python3-pip


## add admindojo to path
echo 'PATH=$PATH:/home/vagrant/.local/bin/'>>/home/vagrant/.bashrc
