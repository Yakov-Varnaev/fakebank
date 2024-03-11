from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.dependencies.pagination import Pagination
from app.core.exceptions import BadRequest, Forbidden
from app.db.crud import SerializedPage
from app.db.postgres import async_session
from app.transactions.crud import TransactionORM
from app.transactions.exceptions import (InvalidTransaction,
                                         TransactionPermissionError)
from app.transactions.schemas import (TransactionCreateSchema,
                                      TransactionReadSchema)
from app.transactions.services.performer import TransactionPerformer
from app.users.auth import current_active_user
from app.users.models import User

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.post('/')
async def create_transaction(
    request: Request,
    transaction_data: TransactionCreateSchema,
    user: User = Depends(current_active_user),
) -> TransactionReadSchema:

    async with async_session() as db:
        perfomer = TransactionPerformer(
            db, request.app.state.transaction_producer
        )

        try:
            transaction = await perfomer(user.id, transaction_data)
        except InvalidTransaction as e:
            raise BadRequest(detail=str(e))
        except TransactionPermissionError as e:
            raise Forbidden(detail=str(e))
        except Exception as e:
            raise BadRequest(detail=str(e))
        return TransactionReadSchema.model_validate(transaction)


@router.get('/my')
async def get_user_transactions(
    user: User = Depends(current_active_user),
    pagination: Annotated[Pagination, Depends(Pagination)] = Pagination(0, 10),
) -> SerializedPage[TransactionReadSchema]:
    async with async_session() as db:
        orm = TransactionORM(db)
        page = await orm.filter_by_user(user.id).get_page(pagination)
    return page.serialize(TransactionReadSchema)
