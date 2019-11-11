#!/home/yogi/bluedot/randie/bin/python
from nani.src.database import Database
class Commands(object):
    def __init__(self, token, serve, command, tag, response, mac):
        self.token = token
        self.serve = serve
        self.command = command
        self.tag = tag
        self.response = response
        self.mac = mac

    def save_to_mongo(self):
        print("save_to_mongo()")
        Database.update(collection='invaders', query = {'mac': self.mac},
                        data={'$push': {'commands': self.json()}})



    def json(self):
        return {
            'token': self.token,
            'serve': self.serve,
            'command': self.command,
            'tag': self.tag,
            'response': self.response
        }
