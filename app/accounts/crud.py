from typing_extensions import Self

from app.accounts.models import Account
from app.db.crud import BaseORM


class AccountORM(BaseORM[Account]):
    model = Account

    def search(self, query: str) -> Self:
        self.filter(Account.name.ilike(f'%{query}%'))
        return self
