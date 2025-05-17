from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

from flask import render_template_string

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WebCraft Server</title>
  <style>
    body { font-family: sans-serif; background: #111; color: #0f0; text-align: center; padding: 50px; }
    h1 { font-size: 48px; }
    p { font-size: 20px; }
    a { color: #0f0; text-decoration: underline; }
  </style>
</head>
<body>
  <h1>🧱 WebCraft Server</h1>
  <p>Сервер работает! WebCraft готов к подключению.</p>
  <p><a href="https://github.com/Hack6297/WebcraftClient" target="_blank">Скачать клиент</a></p>
</body>
</html>
""")


@socketio.on('place_block')
def handle_place_block(data):
    print(f"Block placed: {data}")
    emit('place_block', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=65432)
