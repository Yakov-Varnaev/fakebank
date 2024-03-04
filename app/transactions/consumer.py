import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer  # type: ignore[import]
from pydantic import UUID4

from app.core.config import settings
from app.db.postgres import async_session
from app.transactions.crud import AccountCRUD, TransactionCRUD
from app.transactions.models import Transaction
from app.transactions.schemas import (TransactionCreateSchema,
                                      TransactionStatusSchema)

logger = logging.getLogger('transaction consumer')


class TransactionError(Exception):
    pass


class NotEnoughBalance(TransactionError):
    message = 'Not enough balance'


class TransactionPipeline:
    def __init__(self, db, transaction_data: TransactionCreateSchema):
        self.transaction_data = transaction_data
        self.db = db

    async def get_account(self, id: UUID4):
        return await AccountCRUD(self.db).get_with_user_data(id=id)

    async def create_transaction(self) -> Transaction:
        return await TransactionCRUD(self.db).create(self.transaction_data)

    async def __process(self):
        status = {}
        try:
            sent_from = await self.get_account(self.transaction_data.sent_from)
            sent_to = await self.get_account(self.transaction_data.sent_to)
            transaction = await self.create_transaction()

            status['sender_account'] = sent_from.id
            status['sender_email'] = sent_from.user.email
            status['sender_id'] = sent_from.user.id
            status['receiver_account'] = sent_to.id
            status['receiver_email'] = sent_to.user.email
            status['receiver_id'] = sent_to.user.id
            status['amount'] = transaction.amount
            status['old_balance'] = None
            status['new_balance'] = None

            if sent_from.balance < transaction.amount:
                status['reason'] = 'Not enough balance'
                transaction.status = 'failed'
            else:
                status['old_balance'] = sent_from.balance

                sent_from.balance -= transaction.amount
                sent_to.balance += transaction.amount

                status['new_balance'] = sent_from.balance

                transaction.status = 'success'
        except TransactionError as e:
            transaction.status = 'failed'
            status['reason'] = e.message
        status['status'] = transaction.status
        return TransactionStatusSchema(**status)

    async def process(self):
        try:
            await self.db.begin()
            logger.info('Processing transaction')
            status = await self.__process()
            await self.db.commit()
            logger.info('Transaction processed successfully')
            return status
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Error while processing transaction: {e}')
        finally:
            await self.db.close()
            logger.info('Database connection closed')


class TransactionProcessor:
    def __init__(self):
        self.kafa_url = settings.kafka_url
        self.transaction_topic = settings.transaction_topic
        self.notifications_topic = settings.notifications_topic
        self.consumer = None
        self.producer = None

    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            self.transaction_topic,
            bootstrap_servers=self.kafa_url,
            value_deserializer=TransactionCreateSchema.model_validate_json,
        )
        self.producer = AIOKafkaProducer(bootstrap_servers=self.kafa_url)
        await self.consumer.start()
        await self.producer.start()
        return self

    async def __aexit__(self, *_):
        await self.consumer.stop()
        await self.producer.stop()


async def consume_transactions():
    async with TransactionProcessor() as processor:
        logger.info('Consuming Transactions')
        async for msg in processor.consumer:
            async with async_session() as db:
                logger.info(f'Log consumed message: {msg.value}')
                result = await TransactionPipeline(db, msg.value).process()
                logger.info(f'Transaction processed. Status: {result}.')
            if result is not None:
                await processor.producer.send(
                    settings.notifications_topic,
                    value=result.model_dump_json().encode(),
                )
                logging.info('Notification sent')


def run_consumer():
    import asyncio

    asyncio.run(consume_transactions())
