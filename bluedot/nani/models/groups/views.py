from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from nani import admin_required
from .group import Group
import nani.models.groups.errors as GroupErrors
import nani.models.users.errors as UserErrors
from nani.models.starter.pretty import stattus


group_blueprint = Blueprint('groups', __name__)


@group_blueprint.route('/add/<string:gname>', methods=['POST'])
@admin_required
def add_group(gname):
    try:
        if Group.create_group(gname):
            return jsonify(message='Successfully Group Added'), 200
    except GroupErrors.GroupAlreadyExistsError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/delete/<string:gname>', methods=['POST'])
@admin_required
def delete_group(gname):
    try:
        if Group.delete_group(gname):
            return jsonify(message='Successfully Group Deleted'), 200
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/active/<string:gname>', methods=['POST'])
@admin_required
def make_group_active(gname):
    try:
        if Group.make_group_active(gname):
            return jsonify(message='Successfully Group is made Active'), 200
    except GroupErrors.GroupAlreadyActiveError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/inactive/<string:gname>', methods=['POST'])
@admin_required
def make_group_inactive(gname):
    try:
        if Group.make_group_inactive(gname):
            return jsonify(message='Successfully Group is made InActive'), 200
    except GroupErrors.GroupAlreadyInActiveError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/addnode/<string:gname>/<string:node>', methods=['POST'])
@admin_required
def add_node_to_group(gname, node):
    try:
        if Group.add_node_to_group(gname, node):
            return jsonify(message='Successfully Node Added to Group'), 200
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400
    except GroupErrors.NodeNotExistsError as e:
        return jsonify(message=e.message), 400
    except GroupErrors.NodeExistsInaGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/delnode/<string:gname>/<string:node>', methods=['POST'])
@admin_required
def del_node_from_group(gname, node):
    try:
        if Group.remove_node_from_group(gname, node):
            return jsonify(message='Successfully Node Removed from Group'), 200
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400
    except GroupErrors.NodeNotExistsError as e:
        return jsonify(message=e.message), 400
    except GroupErrors.NodeNotExistsInaGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/adduser/<string:gname>/<string:user>', methods=['POST'])
@admin_required
def add_user_to_group(gname, user):
    try:
        if Group.add_user_to_group(gname, user):
            return jsonify(message='Successfully User Added to Group'), 200
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except GroupErrors.UserExistsInGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/deluser/<string:gname>/<string:user>', methods=['POST'])
@admin_required
def del_user_from_group(gname, user):
    try:
        if Group.remove_user_from_group(gname, user):
            return jsonify(message='Successfully User Removed from Group'), 200
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400
    except UserErrors.UserNotExistsError as e:
        return jsonify(message=e.message), 400
    except GroupErrors.UserNotExistsInGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/listbyuser', methods=['GET'])     # lists only active groups with that user
@jwt_required
def user_groups():
    user = get_jwt_identity()
    s = []
    grouplist = Group.find_groups_by_user(user)
    for i in grouplist:
        if i.active is True:
            s.append(i.gname)
    return jsonify(message=s), 200


@group_blueprint.route('/nodelist/<string:gname>', methods=['GET'])       # lists online and offline nodes by group
@jwt_required
def node_list(gname):
    user = get_jwt_identity()
    auth = Group.find_user_in_group(gname, user)
    if auth is None:
        return jsonify(message='You are not Authorised for this Group'), 401
    nodes = Group.find_nodes_in_group(gname)
    return jsonify(message=nodes), 200


@group_blueprint.route('/online/nodelist/<string:gname>', methods=['GET'])   # lists only online nodes by group
@jwt_required
def online_node_list(gname):
    user = get_jwt_identity()
    try:
        auth = Group.find_user_in_group(gname, user)
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400
    if auth is None:
        return jsonify(message='You are not Authorised for this Group'), 401
    try:
        nodes = Group.find_nodes_in_group(gname)
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400
    onlinenodes = []
    for i in nodes:
        if stattus(i) is True:
            onlinenodes.append(i)
    return jsonify(message=onlinenodes), 200
