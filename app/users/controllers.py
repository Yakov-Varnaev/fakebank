from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies.pagination import Pagination
from app.db.crud import SerializedPage
from app.db.postgres import async_session
from app.users.auth import auth_backend, current_active_user, fastapi_users
from app.users.crud import UserORM
from app.users.models import User
from app.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()

auth_router = APIRouter(prefix='/auth', tags=['auth'])
users_router = APIRouter(prefix='/users', tags=['users'])

auth_router.include_router(fastapi_users.get_auth_router(auth_backend))
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
auth_router.include_router(fastapi_users.get_reset_password_router())
auth_router.include_router(fastapi_users.get_verify_router(UserRead))
users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@auth_router.get('/authenticated-route')
async def authenticated_route(user: User = Depends(current_active_user)):
    return {'message': f'Hello {user.email}!'}


@users_router.get('/')
async def get_users(
    _: User = Depends(current_active_user),
    search: str | None = None,
    pagination: Annotated[Pagination, Depends(Pagination)] = Pagination(0, 10),
) -> SerializedPage[UserRead]:
    async with async_session() as db:
        orm = UserORM(db)
        if search:
            orm.search(search)
        page = await orm.get_page(pagination)
    return page.serialize(UserRead)


router.include_router(auth_router)
router.include_router(users_router)
