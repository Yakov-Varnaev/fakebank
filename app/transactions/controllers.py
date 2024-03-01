from http import HTTPStatus

from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     WebSocket, WebSocketDisconnect, logger)
from pydantic import UUID4
from typing_extensions import Annotated

from app.core.dependencies.pagination import Pagination
from app.db.postgres import async_session
from app.transactions.crud import AccountCRUD
from app.transactions.producers import send_transaction
from app.transactions.schemas import (AccountCreateSchema,
                                      AccountDBCreateSchema, AccountReadSchema,
                                      TransactionCreateSchema)
from app.users.auth import current_active_user, current_superuser
from app.users.models import User

account_router = APIRouter(prefix='/accounts', tags=['accounts'])
transaction_router = APIRouter(prefix='/transactions', tags=['transactions'])


@account_router.post('/')
async def create_account(
    account_data: AccountCreateSchema,
    user: User = Depends(current_active_user),
) -> AccountReadSchema:
    account_data = AccountDBCreateSchema(
        user_id=user.id, **account_data.model_dump()
    )
    async with async_session() as db:
        account = await AccountCRUD(db).get_or_create(account_data)
    return AccountReadSchema.model_validate(account)


@account_router.get('/my')
async def get_user_accounts(
    pagination: Annotated[Pagination, Depends(Pagination)],
    user: User = Depends(current_active_user),
) -> dict:
    async with async_session() as db:
        accounts = await AccountCRUD(db).list(pagination, user_id=user.id)
        total = await AccountCRUD(db).count(user_id=user.id)
    return {
        'data': [AccountReadSchema.model_validate(a) for a in accounts],
        'total': total,
    }


@account_router.get('/{account_id}')
async def get_account(
    account_id: UUID4, user: User = Depends(current_active_user),
) -> AccountReadSchema:
    async with async_session() as db:
        account = await AccountCRUD(db).get(id=account_id)
        if account is None:
            raise HTTPException(status_code=404)
        if account.user_id != user.id:
            raise HTTPException(status_code=403, detail='Forbidden')
    return AccountReadSchema.model_validate(account)


@account_router.delete('/{account_id}')
async def delete_account(
    account_id: UUID4, user: User = Depends(current_active_user),
) -> Response:
    async with async_session() as db:
        account = await AccountCRUD(db).get_or_404(id=account_id)
        if account.user_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Forbidden'
            )
        await db.delete(account)
        await db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)


@account_router.put('/{account_id}')
async def update_account(
    account_id: UUID4,
    account_data: AccountCreateSchema,
    user: User = Depends(current_active_user),
) -> AccountReadSchema:
    async with async_session() as db:
        account = await AccountCRUD(db).get_or_404(id=account_id)
        if account.user_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Forbidden'
            )
        account = await AccountCRUD(db).update(account, account_data)
    return AccountReadSchema.model_validate(account)


@account_router.get('/')
async def list_accounts(
    pagination: Annotated[Pagination, Depends(Pagination)],
    _: User = Depends(current_superuser),
) -> list[AccountReadSchema]:
    async with async_session() as db:
        result = await AccountCRUD(db).list(pagination)
    return [AccountReadSchema.model_validate(a) for a in result]


@transaction_router.post('/')
async def create_transaction(
    request: Request,
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
        await send_transaction(
            request.app.state.transaction_producer, transaction_request
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return 'OK'


router = APIRouter()
router.include_router(account_router)
router.include_router(transaction_router)
