from flask import Flask
import config
from nani.src.database import Database

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'yogi'

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
app.register_blueprint(appy)
app.register_blueprint(user_blueprint, url_prefix="/users")
