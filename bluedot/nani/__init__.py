from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
import config
from nani.src.database import Database

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'yogi'

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'is_admin': user.is_admin}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

@app.before_first_request
def init_db():
    from nani.models.users.user import User
    Database.initialize(app.config['DATABASE'])
    user_data = Database.count(app.config['USER_COLLECTION'])

    if user_data == 0:
        print('jkjdjn')
        User.register_user(username='admin', password='admin123', is_admin='True')

from nani.models.starter import appy
from nani.models.users.views import user_blueprint
from nani.models.groups.views import group_blueprint
app.register_blueprint(appy)
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(group_blueprint, url_prefix="/group")
