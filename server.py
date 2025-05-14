from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# НОВЫЙ маршрут для проверки
@app.route('/')
def index():
    return "Server is running!"

@socketio.on('place_block')
def handle_place_block(data):
    print(f"Block placed: {data}")
    emit('place_block', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=65432)
