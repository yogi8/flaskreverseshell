from flask import Blueprint, request, jsonify
from nani import app
from nani.src.database import Database

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods = ['POST'])
def login_user():
    request_data = request.get_json()

@user_blueprint.route('register', methods = ['POST'])
def register_user():
    request_data = request.get_json()

@user_blueprint.route('/logout', methods = ['POST'])
def logout_user():
    request_data = request.get_json()

