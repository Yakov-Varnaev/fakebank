from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.users.controllers import router as user_router
from app.transactions.controllers import router as transaction_router
from app.transactions.producers import transaction_producer


@asynccontextmanager
async def lifespan(_: FastAPI):
    await transaction_producer.start()
    try:
        yield
    finally:
        await transaction_producer.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(transaction_router)
