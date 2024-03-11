from aiokafka import AIOKafkaConsumer  # typing: ignore[import-untyped]

from app.core.config import settings
from app.notifications.schemas import NotificationSchema


class NotificationConsumer:
    def __init__(
        self,
        bootstrap_servers: str | list[str] = settings.kafka_url,
        topic: str = settings.notifications_topic,
    ):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id='notification-consumer',
            value_deserializer=NotificationSchema.model_validate_json,
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
