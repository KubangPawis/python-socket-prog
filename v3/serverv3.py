import socket
import threading
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

def show_header():
    print('\nWelcome to RatChat!')
    print('by Lance Alexander Ventura')
    print('_' * 25)
    print()

def receive_message(client):
    while True:
            try:
                recv_data = client.recv(1024).decode(FORMAT)
                if not recv_data:
                    print("Server disconnected.")
                    break
                print(f'\rClient: {recv_data}')
                print('You: ', end='', flush=True)
            except:
                print("Error receiving data.")
                break
    client.close()

def send_message(client):
    while True:
        try:
            print('You: ', end='', flush=True)
            send_data = input()
            if send_data.lower() == '!exit':
                print("Disconnecting...")
                client.close()
                break
            client.send(send_data.encode(FORMAT))
        except:
            print("Error sending data.")
            break
    client.close()

def set_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f'Server is listening on {HOST}: {PORT}...')

    client, addr = server.accept()
    print(f'Connection established with {addr}')

    show_header()
    try:
        receive_thread = threading.Thread(target=receive_message, args=(client,))
        send_thread = threading.Thread(target=send_message, args=(client,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except KeyboardInterrupt:
        print('Server is shutting down...')
    finally:
        client.close()
        server.close()
        print('Server closed...')

if __name__ == '__main__':
    os.system('cls')
    set_server()