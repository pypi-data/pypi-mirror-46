class RFApiError(Exception):
    pass


class TreeException(Exception):
    """  Базовое исключение  """
    pass


class DataNotFound(TreeException):
    pass


class NodeNotFound(DataNotFound):
    pass


class NodeNotInserted(TreeException):
    pass


class NodeTypeNotFound(DataNotFound):
    pass


class UserNotFound(DataNotFound):
    pass
