import logging

from aiokafka import AIOKafkaProducer
from typing_extensions import Self

from app.core.config import settings

logger = logging.getLogger(__name__)


class TransactionProducer:
    def __init__(
        self,
        bootstrap_servers: str | list[str] = settings.kafka_url,
        topic: str = settings.transaction_topic,
    ):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        self.topic = topic

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, value):
        try:
            result = await self.producer.send_and_wait(self.topic, value=value)
        except Exception as e:
            logger.error(f'Error while sending message to Kafka: {e}')
        else:
            logger.info(
                'Message sent to Kafka: '
                f'{result.topic}:{result.partition}:{result.offset}'
            )

    async def __aenter__(self) -> Self:
        await self.start()
        logger.info(f'{self.__class__.__name__} started.')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
        logger.info(f'{self.__class__.__name__} stopped.')
