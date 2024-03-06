from typing import Any

from sqlalchemy import Select, or_
from sqlalchemy.orm import joinedload

from app.accounts.models import Account
from app.db.crud import BaseORM
from app.transactions.models import Transaction
from app.users.models import User


class TransactionORM(BaseORM[Transaction]):
    model = Transaction

    def get_query(self, *select_stmt: Any) -> Select[tuple[Transaction]]:
        return (super().get_query(*select_stmt)).options(
            joinedload(Transaction.sender_account),
            joinedload(Transaction.recipient_account),
            joinedload(Transaction.sender_account, Account.user),
            joinedload(Transaction.recipient_account, Account.user),
        )
