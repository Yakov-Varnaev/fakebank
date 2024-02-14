from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from app.transactions.crud import AccountCRUD
from app.transactions.schemas import AccountCreateSchema
from app.db.postgres import async_session
from app.users.auth import current_active_user
from app.users.models import User


account_router = APIRouter(prefix='/accounts', tags=['accounts'])


@account_router.post('/')
async def create_account(user: User = Depends(current_active_user),):
    account_data = AccountCreateSchema(user_id=user.id)
    async with async_session() as db:
        return await AccountCRUD(db).get_or_create(**account_data.model_dump())


@account_router.get('/')
async def get_user_accounts(user: User = Depends(current_active_user)):
    async with async_session() as db:
        return await AccountCRUD(db).get_all(user_id=user.id)


@account_router.get('/{account_id}')
async def get_account(
    account_id: UUID4, user: User = Depends(current_active_user)
):
    async with async_session() as db:
        account = await AccountCRUD(db).get(id=account_id)
    if account.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    return account


router = APIRouter()
router.include_router(account_router)
