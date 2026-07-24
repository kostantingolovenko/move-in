from fastapi import APIRouter, Path, WebSocketDisconnect, WebSocket
from services.ws_manager import websocket_manager
import asyncio

from database import redis_client

router = APIRouter(
    prefix='/notifications',
    tags=['notifications']
)

@router.websocket('/{user_id}')
async def send_notification(websocket: WebSocket, user_id: int = Path(gt=0)):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    channel_name = f"notifications:{user_id}"
    await pubsub.subscribe(channel_name)

    async def listen_redis():
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data']

                if isinstance(data, bytes):
                    data = data.decode('utf-8')

                await websocket.send_text(data)

    async def listen_socket():
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass

    redis_task = asyncio.create_task(listen_redis())
    socket_task = asyncio.create_task(listen_socket())

    done, pending = await asyncio.wait([redis_task, socket_task], return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()
    await pubsub.unsubscribe(channel_name)