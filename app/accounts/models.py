from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DECIMAL, UUID, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from app.db.postgres import Base
from app.users.models import User


class Account(Base):
    __tablename__ = 'account'
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    user_id = mapped_column(ForeignKey('users.id'))
    name = mapped_column(String, nullable=False)
    balance = mapped_column(DECIMAL, default=Decimal(0))

    user = relationship(User)
