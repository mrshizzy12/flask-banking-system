from flask import Blueprint

errors = Blueprint('errors', __name__)


from . import error_handlers
