from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socketio

app = Ursina()
sio = socketio.Client()

player = FirstPersonController()
player.cursor.visible = True
player.gravity = 0.0
player.speed = 5

others = {}

# === Воксельный блок ===
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='white_cube'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=1
        )

@sio.on('player_update')
def player_u(data):
    for sid, v in data.items():
        if sid == sio.sid:
            continue
        x, y, z = v['x'], v['y'], v['z']
        c = v['color']
        nick = v.get('nickname', 'Player')

        if len(c) == 3:
            c.append(1)

        if sid not in others:
            others[sid] = Entity(
                model='cube',
                position=(x, y, z),
                scale=(1, 2, 1),
                color=color.rgba(*c),
                texture='white_cube',
                name=nick
            )
        else:
            others[sid].position = (x, y, z)
            others[sid].color = color.rgba(*c)

@sio.on('player_remove')
def player_r(data):
    sid = data['sid']
    if sid in others:
        destroy(others[sid])
        del others[sid]

@sio.on('block_update')
def place_block(data):
    Voxel(position=tuple(data['position']), texture='white_cube')

@sio.on('block_remove')
def remove_block(data):
    for e in scene.entities:
        if e.position == tuple(data['position']) and isinstance(e, Voxel):
            destroy(e)
            break

def update():
    sio.emit('player_position', {
        'x': player.x,
        'y': player.y,
        'z': player.z,
        'color': [255, 255, 0],
        'nickname': 'Player'
    })

def input(key):
    if key == 'left mouse down':
        sio.emit('block_update', {'position': [round(player.x + camera.forward.x), round(player.y + camera.forward.y), round(player.z + camera.forward.z)]})
    elif key == 'right mouse down':
        sio.emit('block_remove', {'position': [round(player.x + camera.forward.x), round(player.y + camera.forward.y), round(player.z + camera.forward.z)]})

# === Запуск ===
sio.connect('https://webcraft-launcher-mhyb.onrender.com', transports=['websocket'], socketio_path='/socket.io')
app.run()

