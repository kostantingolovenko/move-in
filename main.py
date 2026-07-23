import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from config import limiter
from routers import listings, auth, users, admin, reviews, favorites, notifications

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(listings.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(reviews.router)
app.include_router(favorites.router)
app.include_router(notifications.router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from fastapi.responses import HTMLResponse

html_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            #messages { background: #f4f4f4; padding: 10px; border-radius: 5px; }
            .msg { color: green; font-weight: bold; margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h2>Панель власника квартири (ID: <span id="user-id"></span>)</h2>
        <div id="messages">Чекаємо на сповіщення...</div>

        <script>
            // Дістаємо ID юзера з URL
            const userId = window.location.pathname.split("/").pop();
            document.getElementById('user-id').textContent = userId;

            // Підключаємося до нашого WebSocket
            const ws = new WebSocket(`ws://localhost:8000/notifications/${userId}`);

            // Що робити, коли прийшло повідомлення
            ws.onmessage = function(event) {
                const messagesDiv = document.getElementById('messages');

                // Парсимо JSON, який прийшов від сервера
                const data = JSON.parse(event.data);

                // Додаємо нове повідомлення на екран
                const newMessage = document.createElement('div');
                newMessage.className = 'msg';
                newMessage.textContent = `🔔 Нове сповіщення: ${data.text}`;

                messagesDiv.appendChild(newMessage);
            };
        </script>
    </body>
</html>
"""


@app.get("/test-ws/{user_id}")
async def get_test_page(user_id: int):
    return HTMLResponse(html_template)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)