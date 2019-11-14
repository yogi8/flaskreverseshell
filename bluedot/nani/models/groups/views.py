from flask import Blueprint, request, jsonify
from nani import app
from nani.src.database import Database
from .group import Group
import nani.models.groups.errors as GroupErrors

group_blueprint = Blueprint('groups', __name__)


@group_blueprint.route('/add/<string:gname>', methods=['POST'])
def add_group(gname):
    try:
        if Group.create_group(gname):
            return jsonify(message='Successfully Group Added'), 200
    except GroupErrors.GroupAlreadyExistsError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/delete/<string:gname>', methods=['POST'])
def delete_group(gname):
    try:
        if Group.delete_group(gname):
            return jsonify(message='Successfully Group Deleted'), 200
    except GroupErrors.GroupNotExistsError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/active/<string:gname>', methods=['POST'])
def make_group_active(gname):
    try:
        if Group.make_group_active(gname):
            return jsonify(message='Successfully Group is made Active'), 200
    except GroupErrors.GroupAlreadyActiveError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/inactive/<string:gname>', methods=['POST'])
def make_group_inactive(gname):
    try:
        if Group.make_group_inactive(gname):
            return jsonify(message='Successfully Group is made InActive'), 200
    except GroupErrors.GroupAlreadyInActiveError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/addnode/<string:gname>/<string:node>', methods=['POST'])
def add_node_to_group(gname, node):
    try:
        if Group.add_node_to_group(gname, node):
            return jsonify(message='Successfully Node Added to Group'), 200
    except GroupErrors.NodeExistsInaGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/delnode/<string:gname>/<string:node>', methods=['POST'])
def del_node_from_group(gname, node):
    try:
        if Group.remove_node_from_group(gname, node):
            return jsonify(message='Successfully Node Removed from Group'), 200
    except GroupErrors.NodeNotExistsInaGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/adduser/<string:gname>/<string:user>', methods=['POST'])
def add_user_to_group(gname, user):
    try:
        if Group.add_user_to_group(gname, user):
            return jsonify(message='Successfully User Added to Group'), 200
    except GroupErrors.UserExistsInGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/deluser/<string:gname>/<string:user>', methods=['POST'])
def del_user_from_group(gname, user):
    try:
        if Group.remove_user_from_group(gname, user):
            return jsonify(message='Successfully User Removed from Group'), 200
    except GroupErrors.UserNotExistsInGroupError as e:
        return jsonify(message=e.message), 400


@group_blueprint.route('/listbyuser/<string:user>', methods=['GET'])   # remove <string:user> after JWT implementation.
def user_groups(user):
    s = []
    grouplist = Group.find_groups_by_user(user)
    for i in grouplist:
        if i['active'] is True:
            s.append(i['gname'])
    return jsonify(message=s), 200


@group_blueprint.route('/nodelist/<string:gname>', methods=['GET'])
def node_list(gname):
    # user needs to be present in that group before query after JWT implementation.
    user = 'JWT'
    auth = Group.find_user_in_group(gname, user)
    if auth is None:
        return jsonify(message='You are not Authorised for this Group'), 401
    nodes = Group.find_nodes_in_group(gname)
    return jsonify(message=nodes), 200
