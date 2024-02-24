from aiokafka import AIOKafkaProducer
from fastapi.logger import logger
from app.core.config import settings
from app.transactions.schemas import TransactionCreateSchema

logger = logger.getChild(__name__)


async def send_transaction(
    producer: AIOKafkaProducer, transaction: TransactionCreateSchema
):
    logger.info(f'Sending transaction: {transaction}')
    try:
        await producer.send_and_wait(
            settings.transaction_topic,
            value=transaction.model_dump_json().encode(),
        )
    except Exception as e:
        logger.error(f'Error while sending transaction: {e}')
        raise Exception
    else:
        logger.info('Transaction sent succcessfully.')
