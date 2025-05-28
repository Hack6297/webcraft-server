from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp

# Создаём Socket.IO сервер с указанием CORS
sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# FastAPI-приложение
fastapi_app = FastAPI()

# Добавим простой маршрут для проверки статуса
@fastapi_app.get("/")
def index():
    return {"status": "WebCraft multiplayer server is live!"}

# Оборачиваем FastAPI в ASGI-приложение Socket.IO
app = ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path="/socket.io")

# Игроки
players = {}

@sio.event
async def player_position(sid, data):
    if sid in players:
        players[sid].update({
            'x': data['x'],
            'y': data['y'],
            'z': data['z'],
            'color': data['color'],
            'nickname': data.get('nickname', players[sid].get('nickname', 'Player'))
        })
    else:
        # safety fallback
        players[sid] = {
            'x': data['x'],
            'y': data['y'],
            'z': data['z'],
            'color': data['color'],
            'nickname': data.get('nickname', 'Player')
        }

    await sio.emit('player_update', players)

    }
    await sio.emit('player_update', players)

@sio.event
async def block_update(sid, data):
    await sio.emit('block_update', data, skip_sid=sid)

@sio.event
async def block_remove(sid, data):
    await sio.emit('block_remove', data, skip_sid=sid)
