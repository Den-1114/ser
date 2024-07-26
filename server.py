import socket
import threading

HEADER = 4096
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
DISCONNECT_MESSAGE = '!DISCONNECT'
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []

def broadcast(msg, addr):
    message = f"\n[{addr}] : {msg}"
    for client in clients:
        client.send(message.encode(FORMAT))

def handle_client(conn, addr):
    print(f"[USER CONNECTED]: {addr}")
    broadcast(f"has joined the chat!", addr)
    connected = True

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT).strip()
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}]: {msg}")
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    broadcast(msg, addr)
        except Exception as e:
            print(f"Error: {e}")
            connected = False

    conn.close()
    clients.remove(conn)
    print(f"[USER DISCONNECTED]: {addr}")

def start():
    print(f"[SERVER LISTENING]: {ADDR}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")

start()
