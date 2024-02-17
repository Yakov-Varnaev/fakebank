from decimal import Decimal
from pydantic import UUID4, BaseModel


class AccountCreateSchema(BaseModel):
    user_id: UUID4


class AccountBase(BaseModel):
    id: UUID4
    balance: Decimal


class AccountReadSchema(AccountCreateSchema, AccountBase):
    pass


class TransactionCreateSchema(BaseModel):
    sent_from: UUID4
    sent_to: UUID4
    amount: Decimal
