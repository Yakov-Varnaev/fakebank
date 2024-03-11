from app.db.crud import BaseORM
from app.notifications.models import Notification


class NotificationORM(BaseORM):
    model = Notification
