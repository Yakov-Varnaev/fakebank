import logging
from fastapi.responses import HTMLResponse
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)
from pydantic import UUID4
from app.transactions.schemas import TransactionStatusSchema

from app.users.auth import auth_backend, current_active_user, get_user_manager
from app.users.models import User

logger = logging.getLogger(__name__)


router = APIRouter(prefix='/notifications', tags=['notifications'])

html = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: %s<span id="ws-id"></span></h2>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket(
                `ws://localhost:8000/notifications/ws/`
            );
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
'''


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID4, WebSocket] = {}

    async def connect(self, user_id: UUID4, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: UUID4):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, user_id: UUID4, message: str):
        if ws := self.active_connections.get(user_id):
            await ws.send_text(message)
            return
        else:
            logger.info(f'Connection for user {user_id} not found')

    async def broadcast(self, user_ids: list[UUID4], message: str):
        for user_id in user_ids:
            await self.send_personal_message(user_id, message)


manager = ConnectionManager()


async def get_user_from_cookie(
    websocket: WebSocket, user_manager=Depends(get_user_manager)
):
    cookie = websocket.cookies.get('fastapiusersauth')
    strat = await auth_backend.get_strategy()
    user = await strat.read_token(cookie, user_manager)
    if not user or not user.is_active:
        raise WebSocketException('Invalid user')
    yield user


@router.websocket('/ws/')
async def notifications_ws(
    websocket: WebSocket, user=Depends(get_user_from_cookie)
) -> None:
    await manager.connect(user.id, websocket)
    try:
        logger.info(f'User {user.id} connected to websocket')
        async for msg in websocket.app.state.notifications_consumer:
            data = TransactionStatusSchema.model_validate_json(msg.value)
            logger.info(f'Received message: {data}')
            await manager.broadcast(
                [data.receiver_id, data.sender_id], str(data)
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get('/')
async def get(user: User = Depends(current_active_user)):
    return HTMLResponse(html % user.email)
