from fastapi import FastAPI
from app.users.controllers import router as user_router
from app.transactions.controllers import router as transaction_router

app = FastAPI()

app.include_router(user_router)
app.include_router(transaction_router)
