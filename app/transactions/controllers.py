from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from app.transactions.crud import AccountCRUD
from app.transactions.schemas import (
    AccountCreateSchema,
    AccountReadSchema,
    TransactionCreateSchema,
)
from app.transactions.producers import send_transaction
from app.db.postgres import async_session
from app.users.auth import current_active_user, current_superuser
from app.users.models import User


account_router = APIRouter(prefix='/accounts', tags=['accounts'])
transaction_router = APIRouter(prefix='/transactions', tags=['transactions'])


@account_router.post('/')
async def create_account(
    user: User = Depends(current_active_user),
) -> AccountReadSchema:
    account_data = AccountCreateSchema(user_id=user.id)
    async with async_session() as db:
        account = await AccountCRUD(db).get_or_create(
            **account_data.model_dump()
        )
    return AccountReadSchema.from_orm(account)


@account_router.get('/my')
async def get_user_accounts(
    user: User = Depends(current_active_user),
) -> list[AccountReadSchema]:
    async with async_session() as db:
        return await AccountCRUD(db).get_all(user_id=user.id)


@account_router.get('/{account_id}')
async def get_account(
    account_id: UUID4, user: User = Depends(current_active_user)
) -> AccountReadSchema:
    async with async_session() as db:
        account = await AccountCRUD(db).get(id=account_id)
        if account is None:
            raise HTTPException(status_code=404)
        if account.user_id != user.id:
            raise HTTPException(status_code=403, detail='Forbidden')
    return account


@account_router.get('/')
async def list_accounts(
    _: User = Depends(current_superuser),
    skip: int | None = None,
    limit: int | None = None,
) -> list[AccountReadSchema]:
    async with async_session() as db:
        return await AccountCRUD(db).get_list(skip, limit)


@transaction_router.post('/')
async def create_transaction(
    transaction_request: TransactionCreateSchema,
    user: User = Depends(current_active_user),
) -> str:
    async with async_session() as db:
        trans_exists = await AccountCRUD(db).exists(
            user_id=user.id, id=transaction_request.sent_from
        )
    if not trans_exists:
        raise HTTPException(status_code=404, detail='Account not found')
    try:
        await send_transaction(transaction_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return 'OK'


router = APIRouter()
router.include_router(account_router)
router.include_router(transaction_router)
