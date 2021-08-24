from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from celery import Celery
from celery.schedules import crontab
from flask_admin import Admin
from app.utils import MyAdminIndexView


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
admin = Admin(name='Universal Bank', template_mode='bootstrap4', index_view=MyAdminIndexView())
login_manager = LoginManager()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

celery_beat_schedule = {
    '''Executes 1st day of every Month.'''
    "add-every-30-days": {
        "task": "count_interest",
        "schedule": crontab(0, 0, day_of_month='1')
    }
}

def create_app(config_file=Config, initAdmin=True):
    app = Flask(__name__)
    app.config.from_object(config_file)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'please login to access this page!'
    login_manager.login_message_category = 'info'
    
    if initAdmin:
        admin.init_app(app)

    ''' celery worker configuration '''
    celery.conf.update( 
        timezone = app.config['CELERY_TIMEZONE'],
        task_serializer = app.config['CELERY_TASK_SERIALIZER'],
        accept_content = app.config['CELERY_ACCEPT_CONTENT'],
        result_serializer = app.config['CELERY_RESULT_SERIALIZER'],
        beat_schedule = celery_beat_schedule,
    )
   
    ''' register blueprints with application '''
    from app.errors import errors
    app.register_blueprint(errors)
    
    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from app.transactions import transaction
    app.register_blueprint(transaction, url_prefix='/transaction')

    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
    
    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app