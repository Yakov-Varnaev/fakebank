from typing import Any

from pydantic import UUID4
from sqlalchemy import Select, or_
from sqlalchemy.orm import aliased, joinedload

from app.db.crud import BaseCRUD, BaseORM
from app.db.postgres import Base
from app.transactions.models import Account, Transaction
from app.transactions.schemas import (AccountCreateSchema,
                                      AccountDBCreateSchema,
                                      TransactionCreateSchema)


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
        return acc


class AccountORM(BaseORM[Account]):
    model = Account

    def get_object_query(
        self, query: Select[tuple[Account]] | None
    ) -> Select[tuple[Account]]:
        query = query or self.get_query()
        return query.filter(self.model.id == self.kwargs['id'])


class TransactionCRUD(BaseCRUD[Transaction, TransactionCreateSchema]):
    model = Transaction

    async def count_for_user(self, user_id: UUID4) -> int:
        # find Transaction count for user
        account_from_alias = aliased(Account)
        account_to_alias = aliased(Account)
        query = (
            self.get_query()
            .join(
                account_from_alias,
                Transaction.sent_from == account_from_alias.id,
            )
            .join(account_to_alias, Transaction.sent_to == account_to_alias.id)
            .filter(
                or_(
                    account_from_alias.user_id == user_id,
                    account_to_alias.user_id == user_id,
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0
