from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.storage: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.storage[user_id] = websocket

    def disconnect(self, user_id):
        self.storage.pop(user_id, None)

    async def send_personal_message(self, message, user_id):
        websocket = self.storage.get(user_id)
        if websocket:
            await websocket.send_json(message)


websocket_manager = ConnectionManager()