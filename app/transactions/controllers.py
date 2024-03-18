from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.dependencies.pagination import Pagination
from app.db.crud import SerializedPage
from app.db.postgres import async_session
from app.transactions.crud import TransactionORM
from app.transactions.schemas import (TransactionCreateSchema,
                                      TransactionReadSchema)
from app.transactions.services.creator import TransactionCreator
from app.users.auth import current_active_user
from app.users.models import User

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.post('/')
async def create_transaction(
    request: Request,
    transaction_data: TransactionCreateSchema,
    user: User = Depends(current_active_user),
) -> TransactionReadSchema:
    return await TransactionCreator(
        user, transaction_data, request.app.state.transaction_producer
    )()


@router.get('/my')
async def get_user_transactions(
    user: User = Depends(current_active_user),
    pagination: Annotated[Pagination, Depends(Pagination)] = Pagination(0, 10),
) -> SerializedPage[TransactionReadSchema]:
    async with async_session() as db:
        orm = TransactionORM(db)
        page = await orm.filter_by_user(user.id).get_page(pagination)
    return page.serialize(TransactionReadSchema)
