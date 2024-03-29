

class UserError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotExistsError(UserError):
    pass

class IncorrectPasswordError(UserError):
    pass

class UserAlreadyRegisteredError(UserError):
    pass

class UserisAlreadyActiveError(UserError):
    pass

class UserisAlreadyInactiveError(UserError):
    pass

class UserisNotAuthorised(UserError):
    pass