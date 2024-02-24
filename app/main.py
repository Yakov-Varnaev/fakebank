import logging
import argparse
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.core.config import settings
from app.users.controllers import router as user_router
from app.transactions.controllers import router as transaction_router
from app.transactions.views import router as notification_router
from app.transactions.consumer import run_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    transaction_producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_url
    )
    notifications_consumer = AIOKafkaConsumer(
        settings.notifications_topic, bootstrap_servers=settings.kafka_url,
    )
    await notifications_consumer.start()
    await transaction_producer.start()
    app.state.transaction_producer = transaction_producer
    app.state.notifications_consumer = notifications_consumer
    try:
        yield
    finally:
        await transaction_producer.stop()
        await notifications_consumer.stop()


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def index():
    return {'hello': 'world'}


app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(notification_router)


app_by_name = {
    'transactions': run_consumer,
}


logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the service')

    args = parser.parse_args()
    runner = app_by_name[args.name]

    runner()
