import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.config import settings
from app.db.postgres import async_session
from app.users.models import User, get_user_db

cookie_transport = CookieTransport(cookie_max_age=settings.token_lifetime)


async def get_strategy():
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=settings.token_lifetime
    )


auth_backend = AuthenticationBackend(
    name='cookie', transport=cookie_transport, get_strategy=get_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager]:
    yield UserManager(user_db)


async def get_user_by_cookie(cookie) -> User:
    async with async_session() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)
        strategy = await auth_backend.get_strategy()
        user = await strategy.read_token(cookie, user_manager)
        if not user or not user.is_active:
            raise Exception('Invalid user')
        return user


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True)
