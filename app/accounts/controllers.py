from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import UUID4
from typing_extensions import Annotated

from app.accounts.crud import AccountORM
from app.accounts.models import Account
from app.accounts.schemas import AccountCreateSchema, AccountReadSchema
from app.accounts.serivces.creator import AccountCreator
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
    service: Annotated[AccountCreator, Depends(AccountCreator)]
) -> AccountReadSchema:
    account, created = await service()
    if created:
        return Response(
            account.model_dump_json(),
            status_code=HTTPStatus.CREATED,
            media_type='application/json',
        )  # type: ignore[return-value]
    return account


@router.get('/')
async def get_user_accounts(
    query: str | None = None,
    user_id: str | None = None,
    pagination: Annotated[Pagination, Depends(Pagination)] = Pagination(0, 10),
    _: User = Depends(current_active_user),
) -> SerializedPage[AccountReadSchema]:
    async with async_session() as db:
        orm = AccountORM(db)
        if query is not None:
            orm.search(query)
        if user_id:
            orm.filter(Account.user_id == user_id)
        page = await orm.get_page(pagination)
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
