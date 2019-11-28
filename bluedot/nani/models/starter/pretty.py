#!/home/yogi/bluedot/randie/bin/python
from nani.src.database import Database
from datetime import datetime
from nani import app
import nani.models.starter.errors as NodeErrors
collection = app.config['COLLECTION']
group_table = app.config['GROUP_COLLECTION']

print("pretty started")


class Pretty(object):
    def __init__(self, mac):
        self.mac = mac
        self.commands = []
        self.reporte = ''
        # self.active = True

    @staticmethod
    def is_mac_valid(mac):
        data = Database.find_one(collection=collection, query={'mac': mac})
        if data is None:
            raise NodeErrors.NodeNotExistsError('System Does not Exists with that name')
        return True

    def save_to_mongo(self):
        print("save_to_mongo()")
        Database.insert(collection=collection,
                        data=self.json())

    @staticmethod
    def create_node(mac):
        data = Database.find_one(collection=collection, query={'mac': mac})
        if data is not None:
            raise NodeErrors.NodeNotExistsError('System Already Exists with that name')
        Pretty(mac=mac).save_to_mongo()
        return True

    @staticmethod
    def delete_node(mac):
        data = Database.find_one(collection=collection, query={'mac': mac})
        if data is None:
            raise NodeErrors.NodeNotExistsError('System Does not Exists with that name')
        Database.remove(collection=collection, query={'mac': mac})
        Database.updateMany(collection=group_table, query={}, data={'$pull': {'nodes': mac}})
        return True

    @staticmethod
    def make_node_active(mac):
        node_data = Database.find_one(collection=collection, query={'mac': mac})
        if node_data['active'] is True:
            raise NodeErrors.NodeAlreadyActiveError('Node is Already Active')
        Database.update(collection=collection, query={'mac': mac}, data={"$set": {'active': True}})
        return True

    @staticmethod
    def make_node_inactive(mac):
        node_data = Database.find_one(collection=collection, query={'mac': mac})
        if node_data['active'] is False:
            raise NodeErrors.NodeAlreadyInActiveError('Node is Already InActive')
        Database.update(collection=collection, query={'mac': mac}, data={"$set": {'active': False}})
        return True


    def json(self):
        return {
            'mac': self.mac,
            'commands': self.commands,
            'reporte': self.reporte
        }
    # 'active': self.active


def statuss(data):
    # deadline = 60
    deadline = app.config['LASTREACH']
    # print(data['mac'])
    # print(data['reporte'])
    d = data['reporte']
    e = datetime.now()
    f = e - d
    g = int(f.total_seconds())
    if g <= deadline:
        print('router is online')
        return True
    else:
        print('router is offline')
        return False


def stattus(mac):
    data = Database.find_one(collection, {'mac': mac})
    lastreach = app.config['LASTREACH']
    if data is not None:
        # print(data['mac'])
        # print(data['reporte'])
        d = data['reporte']
        e = datetime.now()
        f = e - d
        g = int(f.total_seconds())
        if g <= lastreach:
            return True
        else:
            return False
