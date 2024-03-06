import argparse
import logging
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware

from app.accounts.controllers import router as account_router
from app.transactions.controllers import router as transaction_router
from app.transactions.kafka.consumers import TransactionConsumer
from app.transactions.kafka.producers import TransactionProducer
from app.users.controllers import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Application started.')
    try:
        transaction_producer = TransactionProducer()
        await transaction_producer.start()

        app.state.transaction_producer = transaction_producer
        yield
    finally:
        await transaction_producer.stop()
        logger.info('Application stopped.')


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(account_router)
app.include_router(transaction_router)

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

    uvicorn.run(app, reload=True)


def run_all():
    from concurrent.futures import ProcessPoolExecutor

    runners = [run_app, TransactionConsumer.runner]
    with ProcessPoolExecutor() as executor:
        for runner in runners:
            executor.submit(runner)


app_by_name: dict[str, Callable] = {
    'all': run_all,
    'transactions': TransactionConsumer.runner,
}

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the service')

    args = parser.parse_args()
    runner = app_by_name[args.name]

    runner()
