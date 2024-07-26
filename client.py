import socket
import threading
import time

HEADER = 4096
HOST = '192.168.1.4'
PORT = 5050
ADDR = (HOST, PORT)
DISCONNECT_MESSAGE = '!DISCONNECT'
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message:
                print(message)
        except Exception as e:
            print(f'An error occurred: {e}\nClosing connection...')
            print('Connection closed...')
            client.close()
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            break

def write():
    code = '1234'
    code_input = input('Enter code: ')
    if code_input == code:
        while True:
            message = input()
            send(message)
    else:
        print('Wrong code')
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        client.close()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()
