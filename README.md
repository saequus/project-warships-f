# Project Warships F

Warships Game build with Flask, Celery and RabbitMQ.
RabbitMQ cluster consists of 3 nodes: 
* host rabbitmq at 192.168.33.1 (from inside either VM)
* rabbitmq1 at address 192.168.33.10.
* rabbit2 is at address 192.168.33.11

## Start Vagrant VM and create cluster
* `cd project-warships-f`
* `vagrant up`
* login to rabbit2 `vagrant ssh 192.168.33.11`
* change to root `su sudo -`
* prepare node `sudo rabbitmqctl stop_app`
* and join a cluster `sudo rabbitmqctl join_cluster rabbit@rabbit1`
* `sudo rabbitmqctl start_app`
* logout and send message from host node to cluster `python send_repeat.py 192.168.33.10 5672 any_message_text_here`

## To start game
* Create virtual environment.
* Install dependencies running `pip install -r requirements.txt` in terminal.
* Install and run RabbitMQ server with `rabbitmq-server`.
* Make sure Celery is installed running `celery --version`.
* To start Celery worker, run `celery worker -A app.celery --loglevel=info` from project repository.
* Run `python app.py` from project folder to start Flask app and go to 127.0.0.1:5000 to check things out.

## Notes
* The project is still in development and it's not possible to play yet.
* Python version 3.7.3 is used.
* Tests to be added.

## Links and credits
* [Vagrant](https://www.vagrantup.com/)
* [Creating a RabbitMQ Test Setup With Vagrant](http://seletz.github.io/blog/2012/01/18/creating-a-rabbitmq-test-setup-with-vagrant/)
* [Rabbitmq-vagrant-stuff](https://github.com/pglass/rabbitmq-vagrant-stuff)

