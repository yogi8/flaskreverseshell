#!/home/yogi/flaskk/yogi/bin/python

import pymongo

print("database started")
class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    
    @staticmethod
    def initialize():
        print("database initialised")
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["reverseshell"]
        
    @staticmethod
    def find_one(collection, query):
        print("find_onequery")
        return Database.DATABASE[collection].find_one(query)
    
    @staticmethod
    def update(collection, data):
        Database.DATABASE[collection].update(data)
        
    @staticmethod
    def insert(collection, data):
        print("insert")
        print(collection)
        print(data)
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)
    
    
#hi = Database()
#hi.initialize()
#a=hi.find_one("students" , {"ip":"36"})
#print(a)
#for i in a:
 #   print(i[0])
