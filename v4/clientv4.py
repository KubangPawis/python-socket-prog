import socket
import threading
import time
import sys
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

def show_header(name):
    print('\nConnected to RatChat!')
    print('by Lance Alexander Ventura')
    print('_' * 25)
    print(f'\n[  Hi, {name}!  ]')
    print()

def ask_user_info(client):
    print('\nWelcome to RatChat!')
    print('by Lance Alexander Ventura')
    print('_' * 25)
    print()
    print('Hi new guy! What is your name?\n')

    # Ask for user's name
    print('Enter your name: ', end='', flush=True)
    name = input()
    print(f'Welcome, {name}!\n')
    time.sleep(2)
    os.system('cls')

    # Send the name to the server
    client.send(name.encode(FORMAT))
    return name

def receive_message(client):
    while True:
            try:
                recv_data = client.recv(1024).decode(FORMAT)
                if not recv_data:
                    print("Server disconnected.")
                    break
                print(f'\r{recv_data}')
                print('You: ', end='', flush=True)
            except:
                print("Error receiving data.")
                break
    client.close()

def send_message(client, name):
    while True:
        try:
            print('You: ', end='', flush=True)
            message = input()

            # Check if the message is empty
            if not message:
                sys.stdout.write('\033[1A')  # ANSI ESCAPE CODE to move the cursor up by 1 line!!
                sys.stdout.flush()
                continue

            #  Leave chat command
            if message.lower() == '!exit':
                print("Disconnecting...")
                client.close()
                break

            # Send the message to the server (Though this is dependent on the order)
            client.send(message.encode(FORMAT))
            client.send(name.encode(FORMAT))
        except:
            print("Error sending data.")
            break
    client.close()

def set_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f'Connected to server at: {HOST}: {PORT}')

    name = ask_user_info(client)
    show_header(name)

    try:
        receive_thread = threading.Thread(target=receive_message, args=(client, ))
        send_thread = threading.Thread(target=send_message, args=(client, name))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except KeyboardInterrupt:
        print(f'Client is shutting down...')
    finally:
        client.close()
        print('Client closed.')

if __name__ == '__main__':
    os.system('cls')
    set_client()