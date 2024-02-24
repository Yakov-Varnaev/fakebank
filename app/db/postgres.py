import uuid
from collections.abc import AsyncGenerator
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column
from app.core.config import settings


class Base(DeclarativeBase):
    id = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, nullable=False
    )


engine = create_async_engine(url=settings.db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
