import logging
from collections import defaultdict
from uuid import UUID

from fastapi.websockets import WebSocket
from typing_extensions import Any

logger = logging.getLogger(__name__)


class WebSocketManager:
    active_connections: dict[UUID, list[WebSocket]]

    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, user_id: UUID, ws: WebSocket):
        self.active_connections[user_id].remove(ws)
        try:
            await ws.close()
        except Exception as e:
            logger.error(str(e))

    async def send_personal_message(self, user_id: UUID, message: Any):
        disconnected = []
        for connection in self.active_connections[user_id]:
            try:
                logger.info(
                    f'Sending personal message to {connection} for user: {user_id}'
                )
                await connection.send_json(message)
            except Exception as e:
                logger.error(str(e))
                disconnected.append((user_id, connection))
        for user_id, connection in disconnected:
            await self.disconnect(user_id, connection)

    def is_connected(self, user_id: UUID) -> bool:
        return user_id in self.active_connections
