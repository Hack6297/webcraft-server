import socket
import threading

HOST = '0.0.0.0'
PORT = 65432
clients = []

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                broadcast(msg, conn)
            else:
                remove(conn)
                break
        except:
            break

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
