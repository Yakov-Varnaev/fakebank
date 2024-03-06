from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict

from app.accounts.schemas import AccountReadSchema
from app.users.schemas import UserRead


class TransactionCreateSchema(BaseModel):
    sender: UUID4
    recipient: UUID4
    amount: float


class AccountSchema(BaseModel):
    id: UUID4
    name: str
    user: UserRead

    model_config = ConfigDict(from_attributes=True)


class TransactionReadSchema(BaseModel):
    id: UUID4
    time: datetime
    status: str
    sender_account: AccountSchema
    recipient_account: AccountSchema
    amount: float

    model_config = ConfigDict(from_attributes=True)
