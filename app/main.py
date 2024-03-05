import argparse
import logging
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.accounts.controllers import router as account_router
from app.transactions.controllers import router as transaction_router
from app.users.controllers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def index():
    return {'hello': 'world'}


app.include_router(user_router)
app.include_router(account_router)
app.include_router(transaction_router)

origins = [
    'http://localhost.tiangolo.com',
    'https://localhost.tiangolo.com',
    'http://localhost',
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

app_by_name: dict[str, Callable] = {}

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the service')

    args = parser.parse_args()
    runner = app_by_name[args.name]

    runner()
