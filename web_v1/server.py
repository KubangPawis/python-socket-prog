import socket
import threading
import os

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f'Server running on http://{SERVER}:{PORT}')

def get_mime_type(filename):
    #Determine the MIME type based on file extension.
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        return 'image/jpeg'
    elif filename.endswith('.gif'):
        return 'image/gif'
    else:
        return 'application/octet-stream'

def handle_client(conn, addr):
    request = conn.recv(1024).decode('utf-8')
    print(f'Request from {addr}:\n{request}')

    # In case, a client creates a connection but not send any HTTP request data
    if not request:
        conn.close()
        return
    
    request_line = request.split('\n')[0] # Get the line with the REQUEST METHOD like GET, POST
    parts = request_line.split()
    if len(parts) < 2:
        conn.close()
        return

    file_requested = parts[1] # Get the file name next to the REQUEST METHOD
    print(f'File Requested: {file_requested}')
    
    if file_requested == '/':
        file_requested = 'index.html'
    else:
        file_requested = file_requested.lstrip('/')  # Remove leading '/' for proper file path
        print(f'MODIFIED FILE REQUESTED: {file_requested}')
    file_path = os.path.join(BASE_DIR, 'web', file_requested)

    if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                response_body = file.read()
            
            mime_type = get_mime_type(file_requested)
            response_header = f'HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n'
    else:
        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
        response_body = b'<h1>404 Not Found</h1>'

    # Send the response
    conn.sendall(response_header.encode('utf-8') + response_body)
    conn.close()

def set_server():
    while True:
        conn, addr = server.accept()
        print(f'[NEW CONNECTION] {addr} connected.')
        print()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == '__main__':
    set_server()