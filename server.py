from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
sio_app = ASGIApp(sio)

app = FastAPI()

@app.get("/")
def index():
    return {"status": "WebCraft multiplayer server is live!"}

# Монтируем на /ws, чтобы WebSocket работал надёжно
app.mount("/ws", sio_app)
