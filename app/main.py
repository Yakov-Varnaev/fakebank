import argparse
import logging
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.notifications.kafka.consumer import NotificationConsumer
from app.transactions.kafka.consumers import TransactionConsumer
from app.transactions.kafka.producers import TransactionProducer

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if settings.enable_kafka:
            transaction_producer = TransactionProducer()
            await transaction_producer.start()

            notification_consumer = NotificationConsumer()
            await notification_consumer.start()

            app.state.transaction_producer = transaction_producer
            app.state.notification_consumer = notification_consumer
        yield
    finally:
        if settings.enable_kafka:
            await transaction_producer.stop()
            await notification_consumer.stop()
        logger.info('Application stopped.')


app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix='/api')


def configure_app():
    installed_apps = ['users', 'accounts', 'transactions', 'notifications']
    for app_name in installed_apps:
        router = __import__(f'app.{app_name}.controllers', fromlist=['router'])
        api_router.include_router(router.router)
    app.include_router(api_router)


configure_app()

origins = [
    'http://localhost:8080',
    'http://localhost:7000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def run_app():
    import uvicorn

    uvicorn.run('app.main:app')


app_by_name: dict[str, Callable] = {
    'transactions': TransactionConsumer.runner,
}

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the service')

    args = parser.parse_args()
    runner = app_by_name[args.name]

    runner()
