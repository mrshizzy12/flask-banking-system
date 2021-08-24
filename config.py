import os
import secrets


basedir = os.path.abspath(os.path.dirname(__file__))
TIME_ZONE = "UTC"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///{}'.format(os.path.join(basedir, 'db.sqlite3'))
    
    # set default button sytle and size
    # will be overwritten by macro parameters
    BOOTSTRAP_BTN_STYLE = 'primary'
    BOOTSTRAP_BTN_SIZE = 'md'
    BOOTSTRAP_SERVE_LOCAL = True         
    BOOTSTRAP_BOOTSWATCH_THEME = 'cerulean'

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE

    FLASK_ADMIN_SWATCH = 'cerulean'
    
    ADMINS = ['admin@gmail.com']