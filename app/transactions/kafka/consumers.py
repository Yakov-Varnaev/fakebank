import logging
from uuid import UUID

from aiokafka import AIOKafkaConsumer  # type: ignore[import-untyped]
from aiokafka import AIOKafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Self

from app.core.config import settings
from app.db.postgres import async_session
from app.notifications.models import Notification
from app.notifications.schemas import NotificationSchema
from app.transactions.crud import TransactionORM
from app.transactions.models import Transaction
from app.transactions.services.performer import TransactionPerformer

logger = logging.getLogger(__name__)


class TransactionConsumer:
    db: AsyncSession

    def __init__(
        self,
        bootstrap_servers: str | list[str] = settings.kafka_url,
        topic: str = settings.transaction_topic,
        notifications_topic: str = settings.notifications_topic,
        group_id: str | None = None,
    ):
        self.consumer = AIOKafkaConsumer(
            topic, bootstrap_servers=bootstrap_servers, group_id=group_id,
        )

        self.notifications_topic = notifications_topic
        self.notification_producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers
        )

    async def start(self):
        await self.consumer.start()
        await self.notification_producer.start()

    async def stop(self):
        await self.consumer.stop()
        await self.notification_producer.stop()

    async def __aenter__(self) -> Self:
        await self.start()
        self.db = async_session()
        self.processor = TransactionPerformer(self.db)
        logger.info(f'{self.__class__.__name__} started.')
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.stop()
        await self.db.close()
        logger.info(f'{self.__class__.__name__} stopped.')

    async def consume(self):
        async for msg in self.consumer:
            async with self.db.begin():
                logger.info(
                    '{}:{:d}:{:d}: key={} value={} timestamp_ms={}'.format(
                        msg.topic,
                        msg.partition,
                        msg.offset,
                        msg.key,
                        msg.value,
                        msg.timestamp,
                    )
                )
                transaction_id = UUID(msg.value.decode())
                transaction = (
                    await TransactionORM(self.db)
                    .filter(Transaction.id == transaction_id)
                    .get_one()
                )
                if transaction is None:
                    logger.info(
                        f'Transaction with id {msg.value.decode()} not found!'
                    )
                    continue
                logger.info(
                    f'Processing transaction {transaction.id} {transaction.amount}'
                )
                try:
                    await self.processor.validate_transaction(transaction)
                    await self.processor.process_transaction(transaction)
                except Exception as e:
                    logger.error(str(e), exc_info=True)
                    transaction.status = 'error'
                notifications = await self.create_notifications(transaction)

                self.db.add_all(notifications)
                await self.db.flush()
                for notification in notifications:
                    await self.send_notification(notification)

    async def send_notification(self, notification: Notification):
        print(notification.__dict__)
        data = NotificationSchema.model_validate(notification)
        await self.notification_producer.send(
            self.notifications_topic, value=(data.model_dump_json().encode()),
        )

    def get_self_notification_message(
        self, transaction: Transaction
    ) -> list[Notification]:
        return [
            Notification(
                user_id=transaction.sender_account.user_id,
                message=(
                    f'You transferred {transaction.amount} '
                    f'to {transaction.recipient_account.name}'
                ),
                kind='transaction',
            ),
        ]

    def get_notification_message(
        self, transaction: Transaction
    ) -> list[Notification]:
        return [
            Notification(
                user_id=transaction.recipient_account.user_id,
                message=(
                    f'You received {transaction.amount} '
                    f'from {transaction.sender_account.name}'
                ),
                kind='transaction',
            ),
            Notification(
                user_id=transaction.sender_account.user_id,
                message=(
                    f'You sent {transaction.amount} '
                    f'to {transaction.recipient_account.name}'
                ),
                kind='transaction',
            ),
        ]

    async def create_notifications(
        self, transaction: Transaction
    ) -> list[Notification]:
        is_self_transfer = (
            transaction.sender_account.user_id
            == transaction.recipient_account.user_id
        )

        notifications = (
            self.get_self_notification_message(transaction)
            if is_self_transfer
            else self.get_notification_message(transaction)
        )
        return notifications

    @classmethod
    async def run(cls, *args, **kwargs):
        async with cls(*args, **kwargs) as consumer:
            await consumer.consume()

    @classmethod
    def runner(cls, *args, **kwargs):
        import asyncio

        asyncio.run(cls.run(*args, **kwargs))
