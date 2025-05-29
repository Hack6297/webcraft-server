from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp

# Создаём Socket.IO сервер с указанием CORS
sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# FastAPI-приложение
fastapi_app = FastAPI()

# Простой маршрут для проверки
@fastapi_app.get("/")
def index():
    return {"status": "WebCraft multiplayer server is live!"}

# Оборачиваем FastAPI в ASGI Socket.IO
app = ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path="/socket.io")

# Хранилище игроков
players = {}

@sio.event
async def connect(sid, environ):
    print(f"[+] {sid} connected")
    players[sid] = {
        'x': 0,
        'y': 0,
        'z': 0,
        'color': [255, 255, 255],
        'nickname': 'Player'
    }
    await sio.emit('player_update', players)

@sio.event
async def disconnect(sid):
    print(f"[-] {sid} disconnected")
    players.pop(sid, None)
    await sio.emit('player_update', players)

@sio.event
async def player_position(sid, data):
    # Обновление позиции игрока
    if isinstance(data.get('color'), tuple):
        color = list(data['color'])
    else:
        color = data.get('color', [255, 255, 255])

    players[sid] = {
        'x': data.get('x', 0),
        'y': data.get('y', 0),
        'z': data.get('z', 0),
        'color': color,
        'nickname': data.get('nickname', 'Player')
    }
    await sio.emit('player_update', players)

@sio.event
async def block_update(sid, data):
    await sio.emit('block_update', data, skip_sid=sid)

@sio.event
async def block_remove(sid, data):
    await sio.emit('block_remove', data, skip_sid=sid)
