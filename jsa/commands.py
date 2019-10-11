#!/home/yogi/flaskk/yogi/bin/python
from database import Database
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
        Database.update(collection='invaders',
                        ({'mac': self.mac}, {'$push': {'commands': data=self.json()}}))



     def json(self):
        return {
            'token': self.token,
            'serve': self.serve,
            'command': self.command,
            'tag': self.tag,
            'response': self.response
        }
