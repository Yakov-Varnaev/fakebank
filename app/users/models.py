from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.db.postgres import Base, get_async_session


class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = 'users'
    first_name = Column(String(50))
    last_name = Column(String)

    notifications = relationship('Notification', back_populates='user')


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
