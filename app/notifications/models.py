from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from app.db.postgres import Base


class Notification(Base):
    __tablename__ = 'notifications'
    user_id = mapped_column(ForeignKey('users.id'))
    kind = mapped_column(String, nullable=False)
    message = mapped_column(String, nullable=False)
    extra = mapped_column(JSON, nullable=True)

    user = relationship('User', back_populates='notifications')
