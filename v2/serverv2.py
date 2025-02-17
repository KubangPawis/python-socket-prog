import socket
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

def show_header():
    print('\nWelcome to RatChat!')
    print('by Lance Alexander Ventura')

def set_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)

        server.listen()
        print(f'Server is listening on {HOST}: {PORT}...')

        client, addr = server.accept()
        print(f'Connection established with {addr}')

        show_header()
        try:
            while True:
                # To start the chat, the server must receive a message/prompt from the client FIRST
                msg = client.recv(1024).decode(FORMAT)
                print(f'\nClient: {msg}')

                # Prompt for a response to the client
                response = input('You: ')
                client.send(response.encode(FORMAT))
        except KeyboardInterrupt:
            print('Server is shutting down...')
        finally:
            client.close()
            server.close()
            print('Server closed...')

if __name__ == '__main__':
    os.system('cls')
    set_server()