from typing import Any, Sequence, TypeVar

from pydantic import BaseModel
from sqlalchemy import Delete, Result, Select, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Generic, Self

from app.core.dependencies.pagination import Pagination
from app.core.exceptions import NotFound
from app.db.postgres import Base

ORMModel = TypeVar('ORMModel', bound=Base)
SelectModel = Select[tuple[ORMModel]]
Schema = TypeVar('Schema', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


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

    model: type[ORMModel]
    args_filters: Sequence
    kwargs_filters: dict

    def __init__(self, db: AsyncSession, **kwargs):
        self.db = db
        self.kwargs = kwargs
        self.args_filters = []
        self.kwargs_filters = {}

    async def execute(self, query: Any) -> Result:
        return await self.db.execute(query)

    def get_query(self, *select_stmt: Any) -> Select[tuple[ORMModel]]:
        if not select_stmt:
            select_stmt = (self.model,)
        return select(*select_stmt).select_from(self.model)

    def get_object_query(self, query: Select[tuple[ORMModel]] | None = None):
        return query if query is not None else self.get_query()

    def filter(self, *args_filters: Any, **kwargs_filters: Any) -> Self:
        self.args_filters = args_filters
        self.kwargs_filters = kwargs_filters
        return self

    def apply_filter(self, query: Any) -> Select[tuple[ORMModel]] | Delete:
        return query.filter(*self.args_filters).filter_by(**self.kwargs_filters)

    def get_paginated_query(
        self, pagination: Pagination
    ) -> Select[tuple[ORMModel]]:
        query = self.get_query()
        if pagination.limit:
            query = query.limit(pagination.limit)
        if pagination.offset:
            query = query.offset(pagination.offset)
        return query

    # db requests
    async def create(
        self, schema: CreateSchema, commit: bool = True
    ) -> ORMModel:
        instance = self.model(**schema.model_dump())
        self.db.add(instance)
        if commit:
            await self.db.commit()
            await self.db.refresh(instance)
        return instance

    async def get_or_create(
        self, schema: CreateSchema
    ) -> tuple[ORMModel, bool]:
        instance = await self.filter(**schema.model_dump()).get_one()
        if instance is None:
            instance = await self.create(schema)
            return instance, True
        return instance, False

    async def get_one_or_404(self) -> ORMModel:
        instance = await self.get_one()
        if instance is None:
            raise NotFound()
        return instance

    async def count(self, query: Select[tuple[ORMModel]] | None = None) -> int:
        query = query if query is not None else self.get_query(func.count())
        result = await self.execute(self.apply_filter(query))
        return result.scalar_one()

    async def get_page(self, pagination: Pagination) -> Page:
        """
        This method is responsible for paginated data.
        """
        instances = await self.get_multi(self.get_paginated_query(pagination))
        total = await self.count()
        return Page(data=instances, total=total)

    async def get_multi(
        self, query: Select[tuple[ORMModel]] | None = None
    ) -> Sequence[ORMModel]:
        query = query if query is not None else self.get_query()
        result = await self.execute(self.apply_filter(query))
        return result.scalars().all()

    async def get_one(self) -> ORMModel | None:
        result = await self.execute(self.apply_filter(self.get_object_query()))
        return result.scalar()

    async def delete_instance(self, instance: ORMModel) -> None:
        await self.db.delete(instance)
        await self.db.commit()

    async def delete(self) -> None:
        q = self.apply_filter(delete(self.model))
        await self.execute(q)

    async def update_instance(
        self, instance: ORMModel, data: BaseModel
    ) -> ORMModel:
        for field, value in data.model_dump().items():
            setattr(instance, field, value)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
