from typing import Any, OrderedDict, TypeVar
from typing_extensions import Generic
from pydantic import BaseModel
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from app.db.postgres import Base

ORMModel = TypeVar('ORMModel', bound=Base)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


class BaseCRUD(Generic[ORMModel, CreateSchema]):
    model: type[ORMModel]

    def __init__(self, db: AsyncSession):
        self.db = db

    def get_query(self) -> Select:
        return select(self.model)

    def filter_query(self, query: Query, **kwargs) -> Query[ORMModel]:
        return query.filter_by(**kwargs)

    def paginate_query(
        self, query: Query[ORMModel], offset: int, limit: int
    ) -> Query[ORMModel]:
        return query.offset(offset).limit(limit)

    async def create(self, data: CreateSchema) -> ORMModel:
        instance = self.model(**data.model_dump())
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def exists(self, **filters: Any) -> bool:
        q = self.get_query().filter_by(**filters).exists()
        result = await self.db.execute(select(q))
        return bool(result.scalar())
