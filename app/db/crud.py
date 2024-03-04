from http import HTTPStatus
from typing import Any, Sequence, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Generic, Self

from app.core.dependencies.pagination import Pagination
from app.db.postgres import Base

ORMModel = TypeVar('ORMModel', bound=Base)
SelectModel = Select[tuple[ORMModel]]
Schema = TypeVar('Schema', bound=BaseModel)
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

    async def update(self, instance: ORMModel, data: CreateSchema) -> ORMModel:
        for field, value in data.model_dump().items():
            setattr(instance, field, value)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get_or_404(self, **filters: Any) -> ORMModel:
        instance = await self.get(**filters)
        if instance is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return instance

    async def list(
        self, pagination: Pagination = Pagination(), **filters: Any
    ) -> list[ORMModel]:
        query = self.get_base_query(pagination, **filters)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count(self, **filters: Any) -> int:
        query = (
            select(func.count()).select_from(self.model).filter_by(**filters)
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def exists(self, **filters: Any) -> bool:
        q = self.get_query().filter_by(**filters).exists()
        result = await self.db.execute(select(q))
        return bool(result.scalar())

    async def get_or_create(self, data: CreateSchema) -> ORMModel:
        instance = await self.get(**data.model_dump())
        if instance:
            return instance
        return await self.create(data)


class SerializedPage(BaseModel, Generic[Schema]):
    data: Sequence[Schema]
    total: int


class Page(Generic[ORMModel]):
    def __init__(self, data: Sequence[ORMModel], total: int):
        self.data = data
        self.total = total

    def serialize(self, schema: type[Schema]) -> SerializedPage[Schema]:
        return SerializedPage(
            data=[schema.from_orm(inst) for inst in self.data],
            total=self.total,
        )


class BaseORM(Generic[ORMModel]):
    """
    This class will provide a basic approach for quering data
    from DB.
    """

    def __init__(self, db: AsyncSession, **kwargs):
        self.db = db
        self.kwargs = kwargs

    model: type[ORMModel]

    async def execute(self, query: Select[tuple[Any]]) -> Result:
        return await self.db.execute(query)

    def get_query(self, *select_stmt: Any) -> Select[tuple[ORMModel]]:
        if not select_stmt:
            select_stmt = (self.model,)
        return select(*select_stmt).select_from(self.model)

    def get_object_query(self, query: Select[tuple[ORMModel]] | None):
        return query or self.get_query()

    def filter_query(
        self,
        query: Select[tuple[ORMModel]],
        *args_filters: Any,
        **kwargs_filters: Any
    ) -> Select[tuple[ORMModel]]:
        if args_filters:
            query = query.filter(*args_filters)
        if kwargs_filters:
            pass
        return query

    def get_paginated_query(
        self, pagination: Pagination, *args_filters: Any, **kwargs_filters: Any
    ) -> Select[tuple[ORMModel]]:
        query = self.get_query()
        if pagination.limit:
            query = query.limit(pagination.limit)
        if pagination.offset:
            query = query.offset(pagination.offset)
        return self.filter_query(query, *args_filters, **kwargs_filters)

    async def count(self, query: Select[tuple[ORMModel]] | None = None) -> int:
        query = query if query is not None else self.get_query(func.count())
        result = await self.execute(query)
        return result.scalar_one()

    async def get_page(
        self, pagination: Pagination, *args_filter: Any, **kwargs_filters: Any
    ) -> Page:
        """
        This method is responsible for paginated data.
        """
        instances = await self.get_multi(
            self.get_paginated_query(pagination, *args_filter, **kwargs_filters)
        )
        total = await self.count()
        return Page(data=instances, total=total)

    async def get_multi(
        self, query: Select[tuple[ORMModel]] | None
    ) -> Sequence[ORMModel]:
        query = query if query is not None else self.get_query()
        result = await self.execute(query)
        return result.scalars().all()

    async def get_one(self, *args_filters, **kwargs_filters) -> ORMModel | None:
        query = self.get_object_query(self.get_query())
        if args_filters:
            query = query.filter(*args_filters)
        if kwargs_filters:
            query = query.filter_by(**kwargs_filters)

        result = await self.execute(query)
        return result.scalar_one_or_none()
