from app.accounts.models import Account
from app.db.crud import BaseORM


class AccountORM(BaseORM[Account]):
    model = Account
