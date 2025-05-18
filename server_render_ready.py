from flask import Flask, send_file, render_template_string
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template_string(open("templates/index.html", encoding="utf-8").read())

@app.route('/download')
def download():
    return send_file("client_ursina_with_multiplayer.zip", as_attachment=True, download_name="WebCraft.zip", mimetype='application/zip')

@socketio.on('connect')
def connect():
    print("Client connected")

@socketio.on('disconnect')
def disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
