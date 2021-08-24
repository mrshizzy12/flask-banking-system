from flask import jsonify, g
from app import db
from app.api import api
from app.api.auth import basic_auth, token_auth


@api.post('/tokens')
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@api.delete('/tokens')
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
