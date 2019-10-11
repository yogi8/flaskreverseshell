#!/home/yogi/flaskk/yogi/bin/python
from database import Database

print("pretty started")
class Pretty(object):
    def __init__(self, mac):
        self.mac = mac
        self.commands = []

    def save_to_mongo(self):
        print("save_to_mongo()")
        Database.insert(collection='invaders',
                        data=self.json())

    def json(self):
        return {
            'mac': self.mac,
            'commands': self.commands
        }
