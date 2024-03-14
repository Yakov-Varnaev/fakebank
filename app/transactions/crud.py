from typing import Any
from uuid import UUID

from sqlalchemy import Select, or_
from sqlalchemy.orm import joinedload
from typing_extensions import Self

from app.accounts.models import Account
from app.db.crud import BaseORM
from app.transactions.models import Transaction


class TransactionORM(BaseORM[Transaction]):
    model = Transaction

    def get_query(self, *select_stmt: Any) -> Select[tuple[Transaction]]:
        return (
            super()
            .get_query(*select_stmt)
            .options(
                joinedload(Transaction.sender_account, innerjoin=True),
                joinedload(Transaction.recipient_account, innerjoin=True),
                joinedload(
                    Transaction.sender_account, Account.user, innerjoin=True,
                ),
                joinedload(
                    Transaction.recipient_account, Account.user, innerjoin=True
                ),
            )
            .order_by(Transaction.time.desc())
        )

    def filter_by_user(self, user_id: UUID) -> Self:
        self.filter(
            or_(
                Transaction.sender_account.has(Account.user_id == user_id),
                Transaction.recipient_account.has(Account.user_id == user_id),
            )
        )
        return self
