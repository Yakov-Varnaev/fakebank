from decimal import Decimal

from pydantic import UUID4, BaseModel, ConfigDict


class AccountCreateSchema(BaseModel):
    name: str


class AccountDBCreateSchema(AccountCreateSchema):
    user_id: UUID4


class AccountBase(BaseModel):
    id: UUID4
    balance: Decimal


class AccountReadSchema(AccountCreateSchema, AccountBase):
    balance: float  # type: ignore[assignment]
    model_config = ConfigDict(from_attributes=True)
