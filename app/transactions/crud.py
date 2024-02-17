from typing import Any
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import BaseCRUD
from app.db.postgres import get_async_session
from app.transactions.models import Account, Transaction

from app.transactions.schemas import (
    AccountCreateSchema,
    TransactionCreateSchema,
)


class AccountCRUD(BaseCRUD[Account, AccountCreateSchema]):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db

    def get_query(self):
        return select(Account)

    async def get_all(self, **filters: Any):
        q = self.get_query().filter_by(**filters)
        result = await self.db.execute(q)
        return result.scalars().all()

    async def get_list(
        self,
        offset: int | None = None,
        limit: int | None = None,
        **filters: Any
    ):
        q = self.get_query().filter_by(**filters)
        if offset:
            q = q.offset(offset)
        if limit:
            q = q.limit(limit)

        result = await self.db.execute(q)
        return result.scalars().all()

    async def get(self, **filters: Any):
        query = self.get_query().filter_by(**filters)
        result = await self.db.execute(query)
        return result.scalar()

    async def create(self, data: AccountCreateSchema) -> Account:
        account = Account(**data.model_dump())
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account

    async def get_or_create(self, **filters: Any) -> Account:
        instance = await self.get(**filters)
        if instance:
            return instance
        return await self.create(AccountCreateSchema(**filters))


class TransactionCRUD(BaseCRUD[Transaction, TransactionCreateSchema]):
    model = Transaction
