from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socketio, sys

nickname = "Player"
if len(sys.argv) > 1:
    nickname = sys.argv[1]

app = Ursina()
player = FirstPersonController()
player.gravity = 0.5
Sky()

sio = socketio.Client()
sio.connect(
    'https://webcraft-launcher-mhyb.onrender.com',
    transports=['websocket'],
    socketio_path='/ws/socket.io'
)

voxels, others = {}, {}
colors = [color.white, color.red, color.green, color.blue, color.black, color.yellow, color.gray, color.brown, color.violet]
current_color = colors[0]

def create_voxel(pos, col):
    key = str(pos)
    if key not in voxels:
        voxels[key] = Button(parent=scene, model='cube', position=pos, color=col, texture='white_cube', origin_y=0.5, collider='box')

def remove_voxel(pos):
    key = str(pos)
    if key in voxels:
        destroy(voxels[key])
        del voxels[key]

def update_other(sid, x, y, z, c, n):
    if sid == sio.sid: return
    if sid not in others:
        others[sid] = Entity(model='cube', position=(x,y,z), scale=(1,2,1), color=c, texture='white_cube')
        others[sid].label = Text(text=n, position=(x, y+2.2, z), scale=2, origin=(0,0), background=True)
    else:
        others[sid].position = (x,y,z)
        others[sid].color = c
        others[sid].label.text = n
        others[sid].label.position = (x, y+2.2, z)

@sio.on('block_update')
def block_u(data): create_voxel(tuple(data['position']), color.rgb(*data['color']))

@sio.on('block_remove')
def block_r(data): remove_voxel(tuple(data['position']))

@sio.on('player_update')
def player_u(data): [update_other(k, v['x'], v['y'], v['z'], color.rgb(*v['color']), v['nickname']) for k,v in data.items()]

for x in range(20):
    for z in range(20):
        create_voxel((x, 0, z), color.green)

def update():
    sio.emit('player_position', {
        'x': player.x, 'y': player.y, 'z': player.z,
        'color': (current_color.r, current_color.g, current_color.b),
        'nickname': nickname
    })

def input(key):
    global current_color
    hit = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
    if hit.hit and hasattr(hit.entity, 'position'):
        pos = hit.entity.position
        if key == 'left mouse down':
            build_pos = pos + hit.normal
            create_voxel(build_pos, current_color)
            sio.emit('block_update', {'position': tuple(build_pos), 'color': (current_color.r, current_color.g, current_color.b)})
        elif key == 'right mouse down':
            remove_voxel(pos)
            sio.emit('block_remove', {'position': tuple(pos)})
    if key.isdigit() and 1 <= int(key) <= len(colors):
        current_color = colors[int(key)-1]

app.run()
