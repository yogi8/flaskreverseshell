class NodeError(Exception):
    def __init__(self, message):
        self.message = message


class NodeNotExistsError(NodeError):
    pass


class NodeAlreadyExistsError(NodeError):
    pass

class NodeAlreadyActiveError(NodeError):
    pass

class NodeAlreadyInActiveError(NodeError):
    pass