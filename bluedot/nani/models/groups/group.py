import uuid
from nani import app
from nani.src.database import Database
import nani.models.groups.errors as GroupErrors
collection = app.config['GROUP_COLLECTION']


class Group(object):
    def __init__(self, gname, active=True, nodes=None, users=None, _id=None):
        self.gname = gname
        self.active = active
        self.nodes = [] if nodes is None else nodes
        self.users = [] if users is None else users
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def create_group(gname):
        group_data = Database.find_one(collection, {'gname': gname})
        if group_data is not None:
            raise GroupErrors.GroupAlreadyExistsError("Group Already Exists")
        Group(gname).save_to_db()
        return True

    @staticmethod
    def delete_group(gname):
        group_data = Database.find_one(collection=collection, query={'gname': gname})
        if group_data is None:
            raise GroupErrors.GroupNotExistsError('Group Not Exists')
        Database.remove(collection=collection, query={'gname': gname})
        return True

    @staticmethod
    def make_group_active(gname):
        group_data = Database.find_one(collection=collection, query={'gname': gname})
        if group_data['active'] is True:
            raise GroupErrors.GroupAlreadyActiveError('Group is Already Active')
        Database.update(collection=collection, query={'gname': gname}, data={"$set": {'active': True}})
        return True

    @staticmethod
    def make_group_inactive(gname):
        group_data = Database.find_one(collection=collection, query={'gname': gname})
        if group_data['active'] is False:
            raise GroupErrors.GroupAlreadyInActiveError('Group is Already InActive')
        Database.update(collection=collection, query={'gname': gname}, data={"$set": {'active': False}})
        return True

    @staticmethod
    def add_node_to_group(gname, node):
        node_data = Database.find_one(collection=collection, query={'nodes': node})
        if node_data is not None:
            raise GroupErrors.NodeExistsInaGroupError(node + 'Already Exists in a group')
        Database.update(collection=collection, query={'gname': gname}, data={'$push': {'nodes': node}})
        return True

    @staticmethod
    def add_user_to_group(gname, user):
        user_data = Database.find_one(collection=collection, query={'gname': gname, 'users': user})
        if user_data is not None:
            raise GroupErrors.UserExistsInGroupError('User Already Exists in this group')
        Database.update(collection=collection, query={'gname': gname}, data={'$push': {'users': user}})
        return True

    @staticmethod
    def remove_node_from_group(gname, node):
        node_data = Database.find_one(collection=collection, query={'nodes': node})
        if node_data is None:
            raise GroupErrors.NodeNotExistsInaGroupError(node + 'Not Exists in a group')
        Database.update(collection=collection, query={'gname': gname}, data={'$pull': {'nodes': node}})
        return True

    @staticmethod
    def remove_user_from_group(gname, user):
        user_data = Database.find_one(collection=collection, query={'gname': gname, 'users': user})
        if user_data is None:
            raise GroupErrors.UserNotExistsInGroupError('User Not Exists in this group')
        Database.update(collection=collection, query={'gname': gname}, data={'$pull': {'users': user}})
        return True

    def save_to_db(self):
        Database.insert(collection, self.json())

    def json(self):
        return {
            'gname': self.gname,
            'active': self.active,
            'nodes': self.nodes,
            'users': self.users
        }

    @classmethod
    def find_group_by_node(cls, node):
        group = Database.find_one(collection=collection, query={'nodes': node})
        return cls(**group)

    @classmethod
    def find_groups_by_user(cls, user):
        return [cls(**group) for group in Database.find(collection=collection, query={'users': user})]

    @classmethod
    def find_nodes_in_group(cls, gname):
        group_data = Database.find_one(collection=collection, query={'gname': gname})
        if group_data is None:
            raise GroupErrors.GroupNotExistsError('Group Not Exists')
        return cls(**group_data).nodes

    @staticmethod
    def find_user_in_group(gname, user):
        # in active users can access their groups
        group_data = Database.find_one(collection=collection, query={'gname': gname})
        if group_data is None:
            raise GroupErrors.GroupNotExistsError('Group Not Exists')
        group = Database.find_one(collection=collection, query={'gname': gname, 'users': user})
        return group

    @staticmethod
    def find_user_and_node_in_same_group(node, user):
        group = Database.find_one(collection=collection, query={'nodes': node, 'users': user})
        if group is not None:
            return True
