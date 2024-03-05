from app.db.crud import BaseORM
from app.transactions.models import Transaction


class TransactionORM(BaseORM[Transaction]):
    model = Transaction
