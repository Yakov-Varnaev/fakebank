from fastapi.logger import logger
from aiokafka import AIOKafkaProducer  # type: ignore[import]
from app.core.config import settings
from app.transactions.schemas import TransactionCreateSchema

logger = logger.getChild(__name__)


transaction_producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_url)


async def send_transaction(transaction: TransactionCreateSchema):
    logger.info(f'Sending transaction: {transaction}')
    try:
        await transaction_producer.send_and_wait(
            settings.transaction_topic,
            value=transaction.model_dump_json().encode(),
        )
    except Exception as e:
        logger.error(f'Error while sending transaction: {e}')
        raise Exception
    else:
        logger.info('Transaction sent succcessfully.')
