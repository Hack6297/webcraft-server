
from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp

# Socket.IO server with CORS enabled
sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# FastAPI application
fastapi_app = FastAPI()

@fastapi_app.get("/")
def index():
    return {"status": "WebCraft multiplayer server is live!"}

# ASGI app combining FastAPI and Socket.IO
app = ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path="/socket.io")

# Player state
players = {}

@sio.event
async def connect(sid, environ):
    print(f"[+] {sid} connected")
    players[sid] = {
        'x': 0, 'y': 0, 'z': 0,
        'color': [255, 255, 255, 255],
        'nickname': 'Player'
    }
    await sio.emit('player_update', players)

@sio.event
async def disconnect(sid):
    print(f"[-] {sid} disconnected")
    if sid in players:
        del players[sid]
        await sio.emit('player_update', players)

@sio.event
async def player_position(sid, data):
    color_data = data.get('color', [255, 255, 255])
    if len(color_data) == 3:
        color_data.append(255)

    players[sid] = {
        'x': data['x'],
        'y': data['y'],
        'z': data['z'],
        'color': color_data,
        'nickname': data.get('nickname', 'Player')
    }

    await sio.emit('player_update', players)

@sio.event
async def block_update(sid, data):
    await sio.emit('block_update', data, skip_sid=sid)

@sio.event
async def block_remove(sid, data):
    await sio.emit('block_remove', data, skip_sid=sid)
