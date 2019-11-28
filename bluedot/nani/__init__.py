from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager, get_jwt_claims, verify_jwt_in_request
)
import config
from nani.src.database import Database
from functools import wraps

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'yogi'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access'] # ['access', 'refresh']

jwt = JWTManager(app)
blacklist = set()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['is_admin'] is not True:
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    print(user.is_admin)
    return {'is_admin': user.is_admin}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username


@jwt.expired_token_loader
def expired_token_callback(error):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired',
        'mass': error
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired',
        'mass': error
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required',
        'mass': error
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.before_first_request
def init_db():
    from nani.models.users.user import User
    Database.initialize(app.config['DATABASE'])
    user_data = Database.count(app.config['USER_COLLECTION'])

    if user_data == 0:
        print('jkjdjn')
        User.register_user(username='admin', password='admin123', is_admin=True)

from nani.models.starter.aap import appy
from nani.models.users.views import user_blueprint
from nani.models.groups.views import group_blueprint
app.register_blueprint(appy)
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(group_blueprint, url_prefix="/group")
