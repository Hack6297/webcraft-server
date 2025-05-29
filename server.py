
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from socketio import AsyncServer
from socketio.asgi import ASGIApp

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
fastapi_app = FastAPI()

players = {}

@fastapi_app.get("/", response_class=HTMLResponse)
async def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>WebCraft</title></head>
    <body style="background:#111;color:#fff;text-align:center;margin-top:100px">
    <h1>✅ WebCraft multiplayer server is live!</h1>
    <p>Use the client launcher to connect.</p>
    </body>
    </html>
    '''

app = ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path="/socket.io")

@sio.event
async def connect(sid, environ):
    players[sid] = {'x': 0, 'y': 0, 'z': 0, 'color': [255, 255, 255, 255], 'nickname': 'Player'}
    await sio.emit('player_update', players)

@sio.event
async def disconnect(sid):
    players.pop(sid, None)
    await sio.emit('player_update', players)

@sio.event
async def player_position(sid, data):
    color = data.get('color', [255, 255, 255])
    if len(color) == 3:
        color.append(255)
    players[sid] = {
        'x': data['x'], 'y': data['y'], 'z': data['z'],
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
