#!/home/yogi/bluedot/randie/bin/python
from nani.src.database import Database
from datetime import datetime
from nani import app
collection = app.config['COLLECTION']

print("pretty started")
class Pretty(object):
    def __init__(self, mac):
        self.mac = mac
        self.commands = []
        self.reporte = ''

    def save_to_mongo(self):
        print("save_to_mongo()")
        Database.insert(collection='invaders',
                        data=self.json())

    def json(self):
        return {
            'mac': self.mac,
            'commands': self.commands,
            'reporte': self.reporte
        }

def statuss(data):
    deadline = 60
    print(data['mac'])
    print(data['reporte'])
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
