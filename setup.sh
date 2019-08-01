#!/usr/bin/env bash
sudo mv /home/vagrant/sources.list /etc/apt/sources.list

echo "Vagrant: installing programs..."
sudo apt-get --assume-yes update
sudo apt-get --assume-yes install git vim python-dev python-pip rabbitmq-server

echo "Vagrant: configuring git"
git config --global user.name "Paul Glass"
git config --global user.email "paul.glass@rackspace.com"

sudo chmod +x /home/vagrant/start_node.sh

sudo service rabbitmq-server stop

sudo mv /home/vagrant/rabbitmq.config /etc/rabbitmq/rabbitmq.config
sudo mv /home/vagrant/.erlang.cookie /var/lib/rabbitmq/.erlang.cookie
sudo chown rabbitmq /var/lib/rabbitmq/.erlang.cookie
sudo chmod 600 /var/lib/rabbitmq/.erlang.cookie

sudo service rabbitmq-server start
