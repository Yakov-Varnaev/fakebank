import logging

from aiokafka import AIOKafkaConsumer
from typing_extensions import AsyncGenerator, Self

from app.core.config import settings

logger = logging.getLogger(__name__)


class TransactionConsumer:
    def __init__(
        self,
        bootstrap_servers: str | list[str] = settings.kafka_url,
        topic: str = settings.transaction_topic,
        group_id: str | None = None,
    ):
        self.consumer = AIOKafkaConsumer(
            topic, bootstrap_servers=bootstrap_servers, group_id=group_id,
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def __aenter__(self) -> Self:
        await self.start()
        logger.info(f'{self.__class__.__name__} started.')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
        logger.info(f'{self.__class__.__name__} stopped.')

    async def consume(self) -> AsyncGenerator:
        async for msg in self.consumer:
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
            yield msg

    @classmethod
    async def run(cls, *args, **kwargs):
        async with cls(*args, **kwargs) as consumer:
            async for _ in consumer.consume():
                pass

    @classmethod
    def runner(cls, *args, **kwargs):
        import asyncio

        asyncio.run(cls.run(*args, **kwargs))
