# Project Warships F

Warships Game build with Flask, Celery and RabbitMQ.

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

