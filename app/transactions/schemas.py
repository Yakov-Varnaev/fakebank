from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict


class TransactionCreateSchema(BaseModel):
    sender: UUID4
    recipient: UUID4
    amount: float


class TransactionReadSchema(TransactionCreateSchema):
    id: UUID4
    time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
