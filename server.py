import socket
import threading

HOST = '127.0.0.1'
PORT = 55555
num_clients = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []

def start_server():
    server.listen()
    print(f'Server is listening on {HOST}:{PORT}')

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        print(f'New client connected: {addr}')

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def handle_client(conn, addr):
    global num_clients
    num_clients += 1
    print(f'New connection from {addr}. Number of clients: {num_clients}')
    
    
    while True:
        try:
            message = conn.recv(1024)
            print(f'{addr}: {message}')
            if not message:
                remove_client(conn)
                num_clients -= 1
                print(f'Number of clients: {num_clients}')
                break
            broadcast(message, conn)
        except:
            remove_client(conn)
            num_clients -= 1
            print(f'Number of clients: {num_clients}')
            break

def remove_client(conn):
    clients.remove(conn)
    print('Client disconnected')

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

start_server()
