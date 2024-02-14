from decimal import Decimal
from uuid import uuid4
from sqlalchemy import ForeignKey, UUID, DECIMAL
from sqlalchemy.orm import mapped_column
from app.db.postgres import Base


class Account(Base):
    __tablename__ = 'account'
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    user_id = mapped_column(ForeignKey('user.id'))
    balance = mapped_column(DECIMAL, default=Decimal(0))
