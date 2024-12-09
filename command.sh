#!/bin/bash

sudo /etc/init.d/my_iptables_off.sh
sudo apt update
sudo apt install -f -y chromium-chromedriver
sudo /etc/init.d/my_iptables_on.sh

source ~/venv/py3.10.12/bin/activate
pip3 install -r requirements.txt
