from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import (DECIMAL, UUID, CheckConstraint, DateTime, ForeignKey,
                        String)
from sqlalchemy.orm import mapped_column, relationship

from app.db.postgres import Base
from app.users.models import User


class Account(Base):
    __tablename__ = 'account'
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    user_id = mapped_column(ForeignKey('user.id'))
    name = mapped_column(String, nullable=False)
    balance = mapped_column(DECIMAL, default=Decimal(0))

    user = relationship(User)


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = (
        CheckConstraint('amount > 0'),
        CheckConstraint('sent_from != sent_to'),
    )

    id = mapped_column(UUID, primary_key=True, default=uuid4)
    sent_from = mapped_column(ForeignKey('account.id'), nullable=False)
    sent_to = mapped_column(ForeignKey('account.id'), nullable=False,)
    amount = mapped_column(DECIMAL, nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    status = mapped_column(String, default='pending')

    account_from = relationship(Account, foreign_keys=[sent_from])
    account_to = relationship(Account, foreign_keys=[sent_to])
