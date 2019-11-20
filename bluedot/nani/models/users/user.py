import uuid
import nani.models.users.errors as UserErrors
from .utils import Utils
from nani.src.database import Database
from nani import app
collection = app.config['USER_COLLECTION']
print('test user.py' + collection)


class User:
    def __init__(self, username, password, active=True, is_admin=False, _id=None):
        self.username = username
        self.password = password
        self.active = active
        self.is_admin = is_admin
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Username {}>".format(self.username)

    @classmethod
    def is_login_valid(cls, username, password):
        user_data = Database.find_one(collection, {'username': username})

        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")

        if user_data['active'] is False:
            raise UserErrors.UserisNotAuthorised("You are not authorised to Log In")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your Password was wrong")

        return cls(**user_data)

    @staticmethod
    def register_user(username, password, **kwargs):
        user_data = Database.find_one(collection, {'username': username})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("Username Already Exists")

        User(username, Utils.hash_password(password), **kwargs).save_to_db()

        return True

    @staticmethod
    def make_user_active(username):
        user_data = Database.find_one(collection, {'username': username})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")
        if user_data['active'] is True:
            raise UserErrors.UserisAlreadyActiveError("User is Already Active")
        Database.update(collection=collection, query={'username': username}, data={"$set": {'active': True}})
        return True

    @staticmethod
    def make_user_inactive(username):
        user_data = Database.find_one(collection, {'username': username})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")
        if user_data['active'] is False:
            raise UserErrors.UserisAlreadyInactiveError("User is Already InActive")
        Database.update(collection=collection, query={'username': username}, data={"$set": {'active': False}})
        return True

    @staticmethod
    def change_username(username, newusername):
        user_data = Database.find_one(collection, {'username': username})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")
        Database.update(collection=collection, query={'username': username}, data={"$set": {'username': newusername}})
        return True

    @staticmethod
    def change_password(username, password):
        user_data = Database.find_one(collection, {'username': username})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")
        Database.update(collection=collection, query={'username': username},
                        data={"$set": {'password': Utils.hash_password(password)}})
        return True

    @staticmethod
    def delete_user(username):
        user_data = Database.find_one(collection, {'username': username})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")
        Database.remove(collection=collection, query={'username': username})
        return True

    def save_to_db(self):
        Database.insert(collection, self.json())

    def json(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'active': self.active,
            'is_admin': self.is_admin
        }
