from fastapi import Depends

from app.accounts.crud import AccountORM
from app.accounts.schemas import (AccountCreateSchema, AccountDBCreateSchema,
                                  AccountReadSchema)
from app.core.service import BaseService
from app.users.auth import current_active_user
from app.users.models import User


class AccountCreator(BaseService[tuple[AccountReadSchema, bool]]):
    def __init__(
        self,
        account_data: AccountCreateSchema,
        user: User = Depends(current_active_user),
    ):
        self.account_data = account_data
        self.user = user

    async def act(self) -> tuple[AccountReadSchema, bool]:
        account, created = await AccountORM(self.db).get_or_create(
            AccountDBCreateSchema(
                user_id=self.user.id, **self.account_data.model_dump()
            )
        )
        return AccountReadSchema.model_validate(account), created
