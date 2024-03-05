from decimal import Decimal

from fastapi import APIRouter, Depends

from app.accounts.crud import AccountORM
from app.accounts.models import Account
from app.core.exceptions import BadRequest
from app.db.postgres import async_session
from app.transactions.crud import TransactionORM
from app.transactions.schemas import (TransactionCreateSchema,
                                      TransactionReadSchema)
from app.users.auth import current_active_user
from app.users.models import User

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.post('/')
async def create_transaction(
    transaction_data: TransactionCreateSchema,
    user: User = Depends(current_active_user),
) -> TransactionReadSchema:

    async with async_session() as db:
        async with db.begin():
            account_orm = AccountORM(db)
            transaction_orm = TransactionORM(db)
            sender_account = await account_orm.filter(
                Account.id == transaction_data.sender,
                Account.user_id == user.id,
            ).get_one_or_404()
            recipient_account = await account_orm.filter(
                Account.id == transaction_data.recipient
            ).get_one_or_404()

            if sender_account.id == recipient_account.id:
                raise BadRequest('Sender and recipient accounts are the same.')

            if sender_account.balance < transaction_data.amount:
                raise BadRequest('Insufficient funds.')

            sender_account.balance -= Decimal(transaction_data.amount)
            recipient_account.balance += Decimal(transaction_data.amount)
            transaction = await transaction_orm.create(
                transaction_data, commit=False
            )
    return TransactionReadSchema.from_orm(transaction)
