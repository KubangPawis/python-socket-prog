import socket
import threading
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
client_dict = {}

def show_header():
    print('\nWelcome to RatChat!')
    print('by Lance Alexander Ventura')
    print('_' * 25)
    print()

def receive_message(client):
    while True:
            try:
                recv_msg = client.recv(1024).decode(FORMAT)
                name = client.recv(1024).decode(FORMAT)
                print(f'{name}: {recv_msg}')
                send_msg = f'{name}: {recv_msg}'

                # Send to everyone that is not the sender
                for i in client_dict:
                    if i != client:
                        print(i)
                        i.send(send_msg.encode(FORMAT))
                
            except:
                print("Error receiving data.")
                break
    client.close()

def set_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f'Server is listening on {HOST}: {PORT}...')
    show_header()

    try:
        while True:
            # Keep accepting connections
            client, addr = server.accept()
            print(f'Connection established with {addr}')

            # Receive the name of the client
            name = client.recv(1024).decode(FORMAT)
            client_dict[client] = name

            receive_thread = threading.Thread(target=receive_message, args=(client,))
            receive_thread.start()

    except KeyboardInterrupt:
        print('Server is shutting down...')
    finally:
        client.close()
        server.close()
        print('Server closed...')

if __name__ == '__main__':
    os.system('cls')
    set_server()