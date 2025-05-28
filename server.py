from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()

@app.get("/")
def index():
    return {"status": "WebCraft multiplayer server is live!"}

# WebSocket на /ws
app.mount("/ws", ASGIApp(sio))
