from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

Sky()

window.borderless = False
window.fullscreen = True
window.title = 'WebCraft Multiplayer v0.1' # Made in 16.05.2025 (game)
window.color = color.rgb(135, 206, 235)

player = FirstPersonController()
player.cursor.visible = True

available_colors = [
    color.white, color.red, color.green, color.blue,
    color.yellow, color.pink, color.azure, color.orange,
    color.brown, color.violet
]

selected_color_index = 0
selected_color = available_colors[selected_color_index]

# Словарь всех блоков
voxels = {}  # {(x,y,z): Entity}

# Создание земли (террейна)
terrain_size = 20
for x in range(terrain_size):
    for z in range(terrain_size):
        pos = Vec3(x, 0, z)
        block = Entity(
            model='cube',
            texture='white_cube',
            color=color.green,
            position=pos,
            scale=1,
            collider='box'
        )
        voxels[tuple(pos)] = block

# Управление
def input(key):
    global selected_color_index, selected_color

    # Переключение цвета блоков
    if key in ['1','2','3','4','5','6','7','8','9','0']:
        selected_color_index = 9 if key == '0' else int(key) - 1
        selected_color = available_colors[selected_color_index]
        print(f"Selected color: {selected_color}")

    # Строим блок
    if key == 'left mouse down':
        hit = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
        if hit.hit:
            pos = hit.entity.position + hit.normal
            pos = Vec3(round(pos.x), round(pos.y), round(pos.z))
            if tuple(pos) not in voxels and distance(pos, player.position) > 1.5:
                block = Entity(
                    model='cube',
                    texture='white_cube',
                    color=selected_color,
                    position=pos,
                    scale=1,
                    collider='box'
                )
                voxels[tuple(pos)] = block

    # Разрушаем блок
    if key == 'right mouse down':
        hit = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
        if hit.hit:
            pos = hit.entity.position
            pos = Vec3(round(pos.x), round(pos.y), round(pos.z))
            if tuple(pos) in voxels:
                destroy(voxels[tuple(pos)])
                del voxels[tuple(pos)]

app.run()
