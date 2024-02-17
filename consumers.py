import logging
from aiokafka import AIOKafkaConsumer  # type: ignore[import]
from app.core.config import settings
from app.db.postgres import async_session
from app.transactions.crud import TransactionCRUD
from app.transactions.schemas import TransactionCreateSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('transaction consumer')


async def consume_transactions():
    consumer = AIOKafkaConsumer(
        settings.transaction_topic, bootstrap_servers=[settings.kafka_url]
    )
    await consumer.start()
    try:
        logger.info('Consuming Transactions')
        async for msg in consumer:
            logger.info(f'Log consumed message: {msg.value.decode()}')
            transaction_data = TransactionCreateSchema.parse_raw(msg.value)
            async with async_session() as db:
                await TransactionCRUD(db).create(transaction_data)
    except Exception as e:
        logger.error(f'Error while consuming transactions: {e}')
    finally:
        await consumer.stop()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_transactions())
