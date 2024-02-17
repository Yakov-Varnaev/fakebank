from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    UUID,
    DECIMAL,
    String,
)
from sqlalchemy.orm import mapped_column
from app.db.postgres import Base


class Account(Base):
    __tablename__ = 'account'
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    user_id = mapped_column(ForeignKey('user.id'))
    balance = mapped_column(DECIMAL, default=Decimal(0))


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
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(String, default='pending')
