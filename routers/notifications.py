from fastapi import APIRouter, Path, WebSocketDisconnect, WebSocket
from services.ws_manager import websocket_manager

router = APIRouter(
    prefix='/notifications',
    tags=['notifications']
)

@router.websocket('/{user_id}')
async def send_notification(websocket: WebSocket, user_id: int = Path(gt=0)):
    await websocket_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(user_id)

