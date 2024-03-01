from decimal import Decimal

from pydantic import UUID4, BaseModel, ConfigDict


class AccountCreateSchema(BaseModel):
    name: str
    balance: Decimal


class AccountDBCreateSchema(AccountCreateSchema):
    user_id: UUID4


class AccountBase(BaseModel):
    id: UUID4
    balance: Decimal


class AccountReadSchema(AccountCreateSchema, AccountBase):
    balance: float  # type: ignore[assignment]
    model_config = ConfigDict(from_attributes=True)


class TransactionCreateSchema(BaseModel):
    sent_from: UUID4
    sent_to: UUID4
    amount: Decimal


class TransactionStatusSchema(BaseModel):
    sender_account: UUID4 | None
    sender_email: str | None
    sender_id: UUID4 | None
    receiver_account: UUID4 | None
    receiver_email: str | None
    receiver_id: UUID4 | None
    status: str | None
    amount: Decimal | None
    old_balance: Decimal | None
    new_balance: Decimal | None
    reason: str | None

    model_config = ConfigDict(strict=False)

    def __str__(self):
        return (
            f'{self.sender_email} sent {self.amount} to {self.receiver_email} '
            f'with status {self.status} {self.reason}'
        )
