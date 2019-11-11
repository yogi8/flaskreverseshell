import uuid
import .errors as UserErrors
from .utils import Utils
from nani.src.database import Database
from nani import app
collection = app.config['USER_COLLECTION']
print('test user.py '+ collection)

class User:
    def __init__(self, username, password, active=True, is_admin=False, _id=None):
        self.username = username
        self.password = password
        self.active = active
        self.is_admin = is_admin
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Username {}>".format(self.username)

    @staticmethod
    def is_login_valid(username, password):
        user_data = Database.find_one(collection, {'username': username})

        if user_data is None:
            raise UserErrors.UserNotExistsError("Your User doesn't Exist")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your Password was wrong")

        return True

    @staticmethod
    def register_user(username, password):
        user_data = Database.find_one(collection, {'username': username})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("Username Already Exists")

        User(username, Utils.hash_password(password)).save_to_db()

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
