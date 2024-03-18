from app.core.exceptions import BadRequest, Forbidden


class TransactionException(BadRequest):
    pass


class InvalidTransaction(TransactionException):
    pass


class TransactionPermissionError(Forbidden):
    pass
