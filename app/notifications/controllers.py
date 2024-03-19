import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket
from typing_extensions import Annotated

from app.core.dependencies.pagination import Pagination
from app.core.websockets import WebSocketManager
from app.db.crud import SerializedPage
from app.db.postgres import async_session
from app.notifications.crud import NotificationORM
from app.notifications.models import Notification
from app.notifications.schemas import NotificationSchema
from app.users.auth import current_active_user, get_user_by_cookie
from app.users.models import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.get('/')
async def get_notifications(
    user: User = Depends(current_active_user),
    pagination: Annotated[Pagination, Depends(Pagination)] = Pagination(0, 10),
) -> SerializedPage[NotificationSchema]:
    async with async_session() as db:
        page = (
            await NotificationORM(db)
            .filter(Notification.user_id == user.id)
            .get_page(pagination)
        )
    return page.serialize(NotificationSchema)


@router.delete('/')
async def clean_notifications(_: User = Depends(current_active_user)):
    pass


@router.delete('/{notification_id}')
async def delete_notification(
    notification_id: UUID, _: User = Depends(current_active_user)
):
    pass


ws_manager = WebSocketManager()


@router.websocket('/ws')
async def notifications_websocket(ws: WebSocket):
    try:
        user = await get_user_by_cookie(ws.cookies.get('fastapiusersauth'))
    except Exception as e:
        await ws.close(reason=str(e))
    else:
        await ws_manager.connect(user.id, ws)
        async for msg in ws.app.state.notification_consumer.consumer:
            logger.info(f'Sending notification to {user.id}')
            await ws_manager.send_personal_message(
                msg.value.user_id, json.loads(msg.value.model_dump_json())
            )
