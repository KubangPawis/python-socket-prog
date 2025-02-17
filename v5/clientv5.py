import socket
import threading
import json
import time
import sys
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

is_in_selection = False
public_msg_arr = []
private_msg_dict = {}
client_arr = []

def show_header(name):
    print('\nConnected to RatChat!')
    print('by Lance Alexander Ventura')
    print('_' * 25)
    print(f'\n[  Hi, {name}!  ]')
    print()

def show_menu(name):
    show_header(name)
    print('[1] Public Chat Room')
    print('[2] Private Message')
    print('[3] Exit')
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
    print(f'\nWelcome, {name}!\n')
    time.sleep(2)
    os.system('cls')

    # Send the name to the server
    client.send(name.encode(FORMAT))
    return name

def receive_message(client):
    global public_msg_arr
    global private_msg_dict
    global client_arr
    while True:
            try:
                recv_data = client.recv(1024).decode(FORMAT)
                if not recv_data:
                    print("Server disconnected.")
                    break

                if recv_data == 'GET_CLIENTS>':
                    print('IN CLIENT...')
                    client_arr = json.loads(client.recv(4096).decode(FORMAT))
                    print(client_arr)
                    continue

                elif recv_data.startswith('MSG_PUBLIC>'):
                    name, message = recv_data.replace('MSG_PUBLIC>', '').split('|', 1)
                    public_msg_arr = json.loads(client.recv(4096).decode(FORMAT))

                elif recv_data.startswith('MSG_PRIVATE>'):
                    name, message = recv_data.replace('MSG_PRIVATE>', '').split('|', 1)
                    private_msg_dict = json.loads(client.recv(4096).decode(FORMAT))

                # If the client is in a SELECTION (not in menu), print the message
                if is_in_selection:
                    print(f'\r{name}: {message}')
                    print('You: ', end='', flush=True)
            except:
                print('Error receiving data.')
                os.system('cls')
                break

def send_message(client, name, message_type, recipient_name=''):
    global public_msg_arr
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
                break

            if message_type == 'PUBLIC':
                send_data = f'MSG_PUBLIC>{name}|{message}' # Send the message to the server
                client.send(send_data.encode(FORMAT))
                public_msg_arr.append(send_data) # add your new message to the CLIENT SIDE record of messages

            elif message_type == 'PRIVATE':
                send_data = f'MSG_PRIVATE>{name}|{recipient_name}|{message}'
                client.send(send_data.encode(FORMAT))

        except Exception as e:
            print('ERROR FROM CLIENT')
            print(e)
            print("Error sending data.")
            break

def set_client():
    global is_in_selection

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    #print(f'Connected to server at: {HOST}: {PORT}')

    name = ask_user_info(client)
    choice = ''

    # Start the receive thread
    receive_thread = threading.Thread(target=receive_message, args=(client, ))
    receive_thread.start()

    while True:
        is_in_selection = False

        os.system('cls')
        show_menu(name)
        choice = input('Enter choice: ')

        if choice == '1':
            is_in_selection = True
            os.system('cls')
            show_header(name)

            # Print the public message history
            for msg in public_msg_arr:
                name, message = msg.replace('MSG_PUBLIC>', '').split('|', 1)
                print(f'{name}: {message}')

            send_thread = threading.Thread(target=send_message, args=(client, name, 'PUBLIC'))        
            send_thread.start()
            send_thread.join()
                    
        elif choice == '2':
            client.send('GET_CLIENTS>'.encode(FORMAT))

            selected_client_name = ''
            has_selected_back = False
            while True:
                os.system('cls')
                show_header(name)

                # Show Client Listing
                filtered_client_arr = [client_name for client_name in client_arr if client_name != name]
                ctr = 1
                for client_name in filtered_client_arr:
                    print(f'[{ctr}] {client_name}')
                    ctr += 1
                print('[x] Go Back')

                print()
                target_client = input(f'Select the client you want to chat with: ')
                if target_client.isdigit() and 0 < int(target_client) <= len(filtered_client_arr):
                    selected_client_name = filtered_client_arr[int(target_client)-1]
                    break
                elif target_client.strip().lower() == 'x':
                    has_selected_back = True
                    break
                else:
                    print('Invalid choice.')
                    time.sleep(2)

            # If user selects the 'x' option, go back to menu
            if has_selected_back:
                continue

            print('\nConnecting to client...')
            time.sleep(2)
            os.system('cls')
            show_header(name)
            print(f'Chatting with: {selected_client_name}\n')
            is_in_selection = True

            send_thread = threading.Thread(target=send_message, args=(client, name, 'PRIVATE', selected_client_name))        
            send_thread.start()
            send_thread.join()

        elif choice == '3':
            client.close()
            print('Client closed.')
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    os.system('cls')
    set_client()