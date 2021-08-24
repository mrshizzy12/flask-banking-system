# Flask Online Banking System

This is an Online Banking Concept created using Python/Flask Web Framework.

## Features

* Create Bank Account.
* Load account Details Using username & password.
* Deposit & Withdraw Money.
* Transaction Detail Page.
* Count Monthly Interest Using Celery.

## Prerequisites

Be sure you have the following installed on your development machine:

+ Python >= 3.6.3
+ Redis Server
+ Git 
+ pip
+ Virtualenv (virtualenvwrapper is recommended)

## Requirements

+ celery
+ Flask
+ Flask-Moment
+ Flask-Migrate
+ Bootstrap-Flask
+ Flask-Sqlalchemy
+ Flask-Login
+ Flask-Admin
+ Flask_Httpauth
+ phonenumbers
+ redis

## Install Redis Server

[Redis Quick Start](https://redis.io/topics/quickstart)

Run Redis server
```bash/cmd
$ redis-server
```

## Project Installation

To setup a local development environment:

Create a virtual environment in which to install Python pip packages. With [virtualenv](https://pypi.python.org/pypi/virtualenv),

```bash/cmd
$ virtualenv venv  or  python3 -m venv env          # create a python virtualenv
$ source env/bin/activate   # activate the Python virtualenv 
$ env\scripts\activate      # for windows
```


## Clone GitHub Project
```bash/cmd
$ (env) git clone https://github.com/mrshizzy12/flask-banking-system

$ (env) cd flask-banking-system
```

## Install development dependencies
```bash/cmd
$ (env) pip install -r requirements.txt  # make sure your virtual environment is activated.
```

## create Database
```bash
$ (env) flask shell
>>> db.create_all()
```

## Run the web application locally

### for windows
```cmd
$ (env) set FLASK_APP=manage.py
$ (env) set FLASK_ENV=development
$ (env) set SECRET_KEY=<choose-your-secret-key>
$ (env) flask run     # 127.0.0.1:5000
```
### for mac/linux
``bash
$ (env) export FLASK_APP=manage.py
$ (env) export FLASK_ENV=development
$ (env) export SECRET_KEY=<choose-your-secret-key>
$ (env) flask run     # 127.0.0.1:5000
```

# Run Celery

### Run Celery worker
(Different Terminal Window with Virtual Environment Activated)
```bash/cmd
$ (env) celery -A celery_worker.celery worker -l info -P solo

### Run Celery beat
(Different Terminal Window with Virtual Environment Activated)
```bash/cmd
$ (env) celery -A celery_worker.celery beat -l info
```