from flask import render_template, request
from app import db
from . import errors
from app.api.errors import error_response as api_error_response

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@errors.app_errorhandler(404)
def page_not_found_error(e):
    if wants_json_response():
        return api_error_response(404)
    return render_template('error/404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('error/500.html'), 500