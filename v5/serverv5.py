import socket
import threading
import json
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
client_dict = {}

public_msg_arr = []
private_msg_dict = {}

def show_header():
    print('\nWelcome to RatChat!')
    print('by Lance Alexander Ventura')
    print('_' * 25)
    print()

def receive_message(client):
    while True:
            try:
                recv_msg = client.recv(1024).decode(FORMAT)

                if recv_msg == 'GET_CLIENTS>':
                    client.send('GET_CLIENTS>'.encode(FORMAT))
                    client_arr = list(client_dict.keys())
                    print(client_arr)
                    client.send(json.dumps(client_arr).encode(FORMAT))

                elif recv_msg.startswith('MSG_PUBLIC>'):
                    name, message = recv_msg.replace('MSG_PUBLIC>', '').split('|', 1)
                    send_msg = f'MSG_PUBLIC>{name}|{message}'
                    print(send_msg)

                    # Keep track of incoming messages, then send them each time a client sends a message
                    public_msg_arr.append(send_msg)

                    # Send to everyone that is NOT the sender
                    for client_name, socket in client_dict.items():
                        if socket != client:
                            socket.send(send_msg.encode(FORMAT))
                            socket.send(json.dumps(public_msg_arr).encode(FORMAT))

                elif recv_msg.startswith('MSG_PRIVATE>'):
                    name, recipient, message = recv_msg.replace('MSG_PRIVATE>', '').split('|', 2)
                    send_msg = f'MSG_PRIVATE>{name}|{message}'
                    print(recv_msg)

                    # Keep track of incoming messages, then send them each time a client sends a message
                    # Initialize message dictionary
                    if name not in private_msg_dict:
                        private_msg_dict[name] = {}

                    if recipient not in private_msg_dict[name]:
                        private_msg_dict[name][recipient] = []

                    private_msg_dict[name][recipient].append(send_msg)

                    print(private_msg_dict)

                    # Send to the recipient
                    if recipient in client_dict:
                        print(f'RECIPIENT: {client_dict[recipient]}')
                        client_dict[recipient].send(send_msg.encode(FORMAT))
                        client_dict[recipient].send(json.dumps(private_msg_dict[name][recipient]).encode(FORMAT))
                    else:
                        client.send(f'ERROR>{recipient} is not online.'.encode(FORMAT))
                             
            except Exception as e:
                print('ERROR FROM SERVER')
                print(e)
                print("Error receiving data.")
                break
    client.close()

def set_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    #print(f'Server is listening on {HOST}: {PORT}...')
    show_header()

    try:
        while True:
            # Keep accepting connections
            client, addr = server.accept()
            print(f'Connection established with {addr}')

            # Receive the name of the client
            name = client.recv(1024).decode(FORMAT)
            client_dict[name] = client

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