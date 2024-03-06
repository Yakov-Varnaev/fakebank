from app.core.exceptions import FakeBankException


class TransactionException(FakeBankException):
    pass


class InvalidTransaction(TransactionException):
    pass


class TransactionPermissionError(TransactionException):
    pass
