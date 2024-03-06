from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (DECIMAL, UUID, CheckConstraint, DateTime, ForeignKey,
                        String)
from sqlalchemy.orm import mapped_column, relationship

from app.accounts.models import Account
from app.db.postgres import Base


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = (
        CheckConstraint('amount > 0'),
        CheckConstraint('recipient != sender'),
    )

    id = mapped_column(UUID, primary_key=True, default=uuid4)
    sender = mapped_column(ForeignKey('account.id'), nullable=False)
    recipient = mapped_column(ForeignKey('account.id'), nullable=False)
    amount = mapped_column(DECIMAL, nullable=False)
    time = mapped_column(DateTime, default=lambda: datetime.now())
    status = mapped_column(String, default='pending')

    sender_account = relationship(Account, foreign_keys=[sender])
    recipient_account = relationship(Account, foreign_keys=[recipient])
