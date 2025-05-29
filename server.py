from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from socketio import AsyncServer
from socketio.asgi import ASGIApp

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
fastapi_app = FastAPI()

# HTML launch page
@fastapi_app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebCraft Launcher</title>
        <style>
            body {
                background-color: #111;
                color: #0f0;
                font-family: Consolas, monospace;
                text-align: center;
                padding-top: 100px;
            }
            button {
                font-size: 20px;
                padding: 10px 30px;
                background-color: #0f0;
                color: #000;
                border: none;
                cursor: pointer;
                border-radius: 10px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>🚀 WebCraft Multiplayer Server is Live!</h1>
        <p>Click the button below to launch the game:</p>
        <button onclick="window.location.href='webcraft://Player/'">Launch WebCraft</button>
    </body>
    </html>
    """

# Socket.IO ASGI wrapper
app = ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path="/socket.io")

# Multiplayer player registry
players = {}

@sio.event
async def connect(sid, environ):
    print(f"[+] {sid} connected")
    players[sid] = {'x': 0, 'y': 0, 'z': 0, 'color': (255, 255, 255), 'nickname': 'Player'}
    await sio.emit('player_update', players)

@sio.event
async def disconnect(sid):
    print(f"[-] {sid} disconnected")
    players.pop(sid, None)
    await sio.emit('player_update', players)

@sio.event
async def player_position(sid, data):
    players[sid] = {
        'x': data['x'],
        'y': data['y'],
        'z': data['z'],
        'color': data['color'],
        'nickname': data.get('nickname', 'Player')
    }
    await sio.emit('player_update', players)

@sio.event
async def block_update(sid, data):
    await sio.emit('block_update', data, skip_sid=sid)

@sio.event
async def block_remove(sid, data):
    await sio.emit('block_remove', data, skip_sid=sid)
