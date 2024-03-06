from decimal import Decimal

from fastapi import FastAPI
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.accounts.crud import AccountORM
from app.accounts.models import Account
from app.core.config import settings
from app.transactions.crud import TransactionORM
from app.transactions.exceptions import (InvalidTransaction,
                                         TransactionPermissionError)
from app.transactions.models import Transaction
from app.transactions.schemas import TransactionCreateSchema


class TransactionPerformer:
    def __init__(self, db: AsyncSession, app: FastAPI):
        self.db = db
        self.app = app
        self.kafka_enabled = settings.enable_kafka
        self.account_orm = AccountORM(db)
        self.transaction_orm = TransactionORM(db)

    async def __call__(
        self, user_id: UUID4, data: TransactionCreateSchema
    ) -> Transaction:
        # TODO: implement remote transaction processing
        async with self.db.begin():
            sender_account = await self.account_orm.filter(
                Account.id == data.sender
            ).get_one()
            if sender_account is None:
                raise InvalidTransaction('Sender account not found.')
            if sender_account.user_id != user_id:
                raise TransactionPermissionError(
                    'You are not allowed to perform this action.'
                )
            if sender_account.id == data.recipient:
                raise InvalidTransaction(
                    'Sender and recipient accounts are the same.'
                )

            recipient_account = await self.account_orm.filter(
                Account.id == data.recipient
            ).get_one()
            if recipient_account is None:
                raise InvalidTransaction('Recipient account not found.')

            transaction = await self.create_transaction(data)
            await self.db.flush()

            # get transaction with sender and recipient accounts
            full_transaction = await self.transaction_orm.filter(
                Transaction.id == transaction.id
            ).get_one()
            if full_transaction is None:
                raise InvalidTransaction('Transaction not found.')
            await self.validate_transaction(full_transaction)
            await self.process_transaction(full_transaction.id)
        return full_transaction

    async def create_transaction(
        self, data: TransactionCreateSchema
    ) -> Transaction:
        return await self.transaction_orm.create(data, commit=False)

    async def validate_transaction(self, transaction: Transaction):
        if transaction.sender_account.id == transaction.recipient_account.id:
            raise InvalidTransaction(
                'Sender and recipient accounts are the same.'
            )

        if transaction.sender_account.balance < transaction.amount:
            raise InvalidTransaction('Insufficient funds.')

    async def process_transaction(self, transaction_id: UUID4):
        transaction = await self.transaction_orm.filter(
            Transaction.id == transaction_id
        ).get_one()
        if transaction is None:
            raise InvalidTransaction('Transaction not found.')
        sender_account = transaction.sender_account
        recipient_account = transaction.recipient_account
        sender_account.balance -= Decimal(transaction.amount)
        recipient_account.balance += Decimal(transaction.amount)
