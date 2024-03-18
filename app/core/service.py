from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Generic, TypeVar

from app.db.postgres import async_session

Produces = TypeVar('Produces')


class BaseService(ABC, Generic[Produces]):
    with_db: bool = True
    db: AsyncSession | None = None

    async def __call__(self) -> Produces:
        if not self.with_db:
            return await self.act()

        async with async_session() as db:
            self.db = db
            return await self.act()

    @abstractmethod
    async def act(self) -> Produces:
        pass
