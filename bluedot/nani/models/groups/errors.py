class GroupError(Exception):
    def __init__(self, message):
        self.message = message


class GroupNotExistsError(GroupError):
    pass


class GroupAlreadyExistsError(GroupError):
    pass


class UserExistsInGroupError(GroupError):
    pass


class NodeExistsInaGroupError(GroupError):
    pass


class UserNotExistsInGroupError(GroupError):
    pass


class NodeNotExistsInaGroupError(GroupError):
    pass


class GroupAlreadyActiveError(GroupError):
    pass


class GroupAlreadyInActiveError(GroupError):
    pass

