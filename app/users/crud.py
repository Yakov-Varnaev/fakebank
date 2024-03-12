from sqlalchemy import func
from typing_extensions import Self

from app.db.crud import BaseORM
from app.users.models import User


class UserORM(BaseORM[User]):
    model = User

    def search(self, search: str) -> Self:
        self.filter(
            User.email.ilike(f'%{search}%')
            | func.concat(User.first_name, ' ', User.last_name).ilike(
                f'%{search}%'
            )
            | func.concat(User.last_name, ' ', User.first_name).ilike(
                f'%{search}%'
            )
        )
        return self
