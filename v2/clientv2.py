import socket
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

def show_header():
    print('\nConnected to RatChat!')
    print('by Lance Alexander Ventura')

def set_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f'Connected to server at: {HOST}: {PORT}')

    show_header()
    try:
        while True:
            # Send message from client first to start the chat with server
            message = input('\nYou: ')
            client.send(message.encode(FORMAT))
            
            # Wait indefinitely for server response
            data = client.recv(1024).decode(FORMAT)
            if not data:
                break
            print(f'Server: {data}')
    except KeyboardInterrupt:
        print(f'Client is shutting down...')
    finally:
        client.close()
        print('Client closed.')

if __name__ == '__main__':
    os.system('cls')
    set_client()