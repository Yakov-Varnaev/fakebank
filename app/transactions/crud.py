from typing import Any

from sqlalchemy.orm import joinedload
from app.db.crud import BaseCRUD
from app.transactions.models import Account, Transaction

from app.transactions.schemas import (
    AccountCreateSchema,
    TransactionCreateSchema,
)


class AccountCRUD(BaseCRUD[Account, AccountCreateSchema]):
    model = Account

    async def get_with_user_data(self, id: Any) -> Account:
        query = (
            self.get_query()
            .where(self.model.id == id)
            .options(joinedload(self.model.user))
        )

        result = await self.db.execute(query)
        acc = result.scalar_one()
        print(acc.id, acc.user.email, acc.user.id, acc.balance)
        return acc


class TransactionCRUD(BaseCRUD[Transaction, TransactionCreateSchema]):
    model = Transaction
