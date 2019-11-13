from flask import Blueprint, request, jsonify
from nani import app
from nani.src.database import Database
from .group import Group
import nani.models.groups.errors as GroupErrors

group_blueprint = Blueprint('groups', __name__)

@group_blueprint.route('/add', methods=['POST'])
def add_group():
    pass

@group_blueprint.route('/delete', methods=['POST'])
def delete_group():
    pass

@group_blueprint.route('/addnode/<string:node>', methods=['POST'])
def add_node_to_group(node):
    pass

@group_blueprint.route('/adduser/<string:user>', methods=['POST'])
def add_user_to_group(user):
    pass

@group_blueprint.route('/delnode/<string:node>', methods=['POST'])
def del_node_from_group(node):
    pass

@group_blueprint.route('/deluser/<string:user>', methods=['POST'])
def del_user_from_group(user):
    pass

@group_blueprint.route('/list/<string:user>', methods=['GET'])   # remove <string:user> after JWT implementation.
def add_group(user):
    s = []
    grouplist = Group.find_groups_by_user(user)
    for i in grouplist:
        if i['active'] == True:
            s.append(i['gname'])
    #return jsonify(message=s)
    pass