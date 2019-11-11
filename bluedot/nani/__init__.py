from flask import Flask
import config
from nani.src.database import Database


app = Flask(__name__)
app.config.from_object('config.Config')

@app.before_first_request
def init_db():
    Database.initialize(app.config['DATABASE'])

from nani.models.starter import appy
app.register_blueprint(appy)
