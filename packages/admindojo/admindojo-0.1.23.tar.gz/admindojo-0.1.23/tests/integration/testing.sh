#!/usr/bin/env bash
cd /home/vagrant/
apt-get install -y python3-venv
pip3 install -i https://test.pypi.org/simple/ admindojo-client --extra-index-url https://pypi.org/simple

admindojo_client
