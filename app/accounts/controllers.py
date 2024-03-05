from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import UUID4
from typing_extensions import Annotated

from app.accounts.crud import AccountORM
from app.accounts.models import Account
from app.accounts.schemas import (AccountCreateSchema, AccountDBCreateSchema,
                                  AccountReadSchema)
from app.core.dependencies.pagination import Pagination
from app.db.crud import SerializedPage
from app.db.postgres import async_session
from app.users.auth import current_active_user
from app.users.models import User

router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.post(
    '/',
    responses={
        HTTPStatus.OK: {
            'model': AccountReadSchema,
            'description': 'Existing account was returned.',
        },
        HTTPStatus.CREATED: {
            'model': AccountReadSchema,
            'description': 'Account was created.',
        },
    },
)
async def create_account(
    account_data: AccountCreateSchema,
    user: User = Depends(current_active_user),
) -> AccountReadSchema:
    account_data = AccountDBCreateSchema(
        user_id=user.id, **account_data.model_dump()
    )
    async with async_session() as db:
        account, created = await AccountORM(db).get_or_create(account_data)
    account_data = AccountReadSchema.model_validate(account)
    if created:
        return JSONResponse(
            account_data, status_code=HTTPStatus.CREATED
        )  # type: ignore[return-value]
    return account_data


@router.get('/my')
async def get_user_accounts(
    pagination: Annotated[Pagination, Depends(Pagination)] = Pagination(0, 10),
    user: User = Depends(current_active_user),
) -> SerializedPage[AccountReadSchema]:
    async with async_session() as db:
        page = (
            await AccountORM(db)
            .filter(Account.user_id == user.id)
            .get_page(pagination)
        )
        return page.serialize(AccountReadSchema)


@router.get('/{account_id}')
async def get_account(
    account_id: UUID4, user: User = Depends(current_active_user),
) -> AccountReadSchema:
    async with async_session() as db:
        account = (
            await AccountORM(db)
            .filter(Account.id == account_id)
            .get_one_or_404()
        )
        if account.user_id != user.id:
            raise HTTPException(status_code=403, detail='Forbidden')
    return AccountReadSchema.model_validate(account)


@router.delete(
    '/{account_id}', responses={HTTPStatus.NO_CONTENT: {'model': None}},
)
async def delete_account(
    account_id: UUID4, user: User = Depends(current_active_user),
):
    async with async_session() as db:
        orm = AccountORM(db)
        account = await orm.filter(Account.id == account_id).get_one_or_404()
        if account.user_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Forbidden'
            )
        await orm.delete_instance(account)

    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.put('/{account_id}')
async def update_account(
    account_id: UUID4,
    account_data: AccountCreateSchema,
    user: User = Depends(current_active_user),
) -> AccountReadSchema:
    async with async_session() as db:
        orm = AccountORM(db)
        account = await orm.filter(Account.id == account_id).get_one_or_404()
        if account.user_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Forbidden'
            )
        account = await orm.update_instance(account, account_data)
    return AccountReadSchema.model_validate(account)