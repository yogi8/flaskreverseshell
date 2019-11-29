#!/home/yogi/bluedot/randie/bin/python
#import os
 
#app_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DATABASE = 'reverseshell'
    COLLECTION = 'invaders'
    USER_COLLECTION = 'users'
    GROUP_COLLECTION = 'groups'
    TIMEOUT = 30
    LASTREACH = 60

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass

