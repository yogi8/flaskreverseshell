from flask import Blueprint, request, jsonify
from nani import app
from nani.src.database import Database
from .user import User
import nani.models.users.errors as UserErrors

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['POST'])   # { 'username': 'yogi', 'password': 'yogi' }
def login_user():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    try:
        if User.is_login_valid(username, password):
            return jsonify(message='Successfully logged in'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserisNotAuthorised as e:
        return jsonify(message=e.message), 401
    except UserErrors.IncorrectPasswordError as e:
        return jsonify(message=e.message), 401


@user_blueprint.route('/register', methods=['POST'])  # { 'username': 'yogi', 'password': 'yogi' }
def register_user():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    try:
        if User.register_user(username, password):
            return jsonify(message='Successfully Registered'), 200
    except UserErrors.UserAlreadyRegisteredError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/logout', methods=['POST'])
def logout_user():
    # request_data = request.get_json()
    pass


@user_blueprint.route('/active/<string:username>', methods=['POST'])
def make_user_active(username):
    try:
        if User.make_user_active(username):
            return jsonify(message='Successfully User is made Active'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserisAlreadyActiveError as e:
        return jsonify(message=e.message), 400
    return True


@user_blueprint.route('/inactive/<string:username>', methods=['POST'])
def make_user_active(username):
    try:
        if User.make_user_inactive(username):
            return jsonify(message='Successfully User is made InActive'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserisAlreadyInactiveError as e:
        return jsonify(message=e.message), 400
    return True
