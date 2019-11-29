from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token, get_raw_jwt,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from nani import admin_required, blacklist
from .user import User
import nani.models.users.errors as UserErrors

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['POST'])   # { 'username': 'yogi', 'password': 'yogi' }
def login_user():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    print(username)
    print(password)

    try:
        user = User.is_login_valid(username, password)
        if user:
            print(user)
            del user.password
            print(user)
            access_token = create_access_token(identity=user, expires_delta=False)
            # refresh_token = create_refresh_token(identity=user)
            return jsonify(access_token=access_token), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserisNotAuthorised as e:
        return jsonify(message=e.message), 401
    except UserErrors.IncorrectPasswordError as e:
        return jsonify(message=e.message), 401


@user_blueprint.route('/register', methods=['POST'])  # { 'username': 'yogi', 'password': 'yogi', 'is_admin': False }
@admin_required
def register_user():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    is_admin = request_data['is_admin'] if 'is_admin' in request_data else False

    try:
        if User.register_user(username, password, is_admin):
            return jsonify(message='Successfully Registered'), 200
    except UserErrors.UserAlreadyRegisteredError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/logout', methods=['POST'])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@user_blueprint.route('/active/<string:username>', methods=['POST'])
@admin_required
def make_user_active(username):
    try:
        if User.make_user_active(username):
            return jsonify(message='Successfully User is made Active'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserisAlreadyActiveError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/inactive/<string:username>', methods=['POST'])
@admin_required
def make_user_inactive(username):
    if username is 'admin':
        return jsonify(message='Admin can not be made InActive'), 400
    try:
        if User.make_user_inactive(username):
            return jsonify(message='Successfully User is made InActive'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserisAlreadyInactiveError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/admin/change_username/<string:username>/<string:new_username>', methods=['POST'])
@admin_required
def change_users_username(username, new_username):
    if username is 'admin':
        return jsonify(message='Admin Username can not be changed'), 400
    try:
        if User.change_username(username, new_username):
            return jsonify(message='Successfully Username is Changed'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/admin/change_password/<string:username>/<string:new_password>', methods=['POST'])
@admin_required
def change_users_password(username, new_password):
    try:
        if User.change_password(username, new_password):
            return jsonify(message='Successfully Password is Changed'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/change_username/<string:new_username>', methods=['POST'])
@jwt_required
def change_username(new_username):
    username = get_jwt_identity()
    if username is 'admin':
        return jsonify(message='Admin Username can not be changed'), 400
    try:
        if User.change_username(username, new_username):
            return jsonify(message='Successfully Username is Changed'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/change_password/<string:new_password>', methods=['POST'])
@jwt_required
def change_password(new_password):
    username = get_jwt_identity()
    try:
        if User.change_password(username, new_password):
            return jsonify(message='Successfully Password is Changed'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400


@user_blueprint.route('/delete/<string:username>', methods=['POST'])
@admin_required
def delete_user(username):
    if username is 'admin':
        return jsonify(message='Admin can not be Deleted'), 400
    try:
        if User.delete_user(username):
            return jsonify(message='User Deleted Successfully'), 200
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
