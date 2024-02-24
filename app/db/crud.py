from typing import Any, OrderedDict, TypeVar
from typing_extensions import Generic
from pydantic import BaseModel
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from app.core.dependencies.pagination import Pagination

from app.db.postgres import Base

ORMModel = TypeVar('ORMModel', bound=Base)
SelectModel = Select[tuple[ORMModel]]
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


class BaseCRUD(Generic[ORMModel, CreateSchema]):
    model: type[ORMModel]

    def __init__(self, db: AsyncSession):
        self.db = db

    def get_query(self) -> SelectModel:
        return select(self.model)

    def filter_query(self, query: SelectModel, **filters: Any) -> SelectModel:
        if not filters:
            return query
        return query.filter_by(**filters)

    def paginate_query(
        self, query: SelectModel, pagination: Pagination
    ) -> SelectModel:
        if pagination.limit:
            query = query.limit(pagination.limit)
        if pagination.offset:
            query = query.offset(pagination.offset)
        return query

    def get_base_query(
        self, pagination: Pagination = Pagination(), **filters: Any
    ) -> SelectModel:
        query = self.get_query()
        query = self.filter_query(query, **filters)
        query = self.paginate_query(query, pagination)
        return query

    async def create(self, data: CreateSchema) -> ORMModel:
        instance = self.model(**data.model_dump())
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get(self, **filters: Any) -> ORMModel | None:
        query = self.get_query().filter_by(**filters)
        result = await self.db.execute(query)
        return result.scalar()

    async def list(
        self, pagination: Pagination = Pagination(), **filters: Any
    ) -> list[ORMModel]:
        query = self.get_base_query(pagination, **filters)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def exists(self, **filters: Any) -> bool:
        q = self.get_query().filter_by(**filters).exists()
        result = await self.db.execute(select(q))
        return bool(result.scalar())

    async def get_or_create(self, data: CreateSchema) -> ORMModel:
        instance = await self.get(**data.model_dump())
        if instance:
            return instance
        return await self.create(data)
