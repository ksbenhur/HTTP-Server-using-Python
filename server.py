import socket
import os
import threading
import argparse
import datetime

# Constants
HOST = "localhost"
threads_count = 0
timeout = 3
access_logs = []

# Parsing command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-root', type=str, default='./webserver_files', help='root directory for docs')
parser.add_argument('-port', type=int, default=9000, help='listening port')
args = parser.parse_args()

PORT = args.port
ROOT_DIR = args.root


# Accepts incoming requests and creates a new thread for each connection
def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        print(f"Server is listening on port {PORT}...")
        while True:
            server_sock.listen()
            conn, client_addr = server_sock.accept()
            print(f"Connection established with {client_addr}")

            global threads_count
            threads_count += 1

            thread = threading.Thread(target=handle_connection, args=(conn, client_addr))
            thread.start()


# Handles the client connection
def handle_connection(conn, client_addr):
    global threads_count, access_logs
    with conn:
        conn.settimeout(1 if threads_count >= 5 else 3)

        while True:
            try:
                data = conn.recv(1024).decode()
                access_logs.append(data)
                request_lines = data.split('\r\n')
                request_elements = request_lines[0].split()
                process_request(request_elements, conn)

            except Exception as e:
                break

        conn.close()
        threads_count -= 1


# Processes HTTP requests
def process_request(parts, conn):
    requested_file = parts[1]
    print(f"Requested file: {requested_file}")

    if requested_file == '/':
        requested_file = '/index.html'

    file_path = os.path.join(ROOT_DIR, requested_file.lstrip('/'))
    print(f"Full file path: {file_path}")  # Debug: Print the resolved file path

    # Special handling for admin.html
    if 'restricted' in requested_file:
        print("Attempt to access admin.html detected.")
        send_error(conn, 403, "Forbidden", "Access to this resource is denied.")
        return

    # Check if the file type is supported
    content_type = get_content_type(file_path)
    if content_type is None:
        print("Unsupported file type.")  # Debug: Log file type check
        send_error(conn, 400, "This Media Type Is Not Supported", "Unsupported file format, please try again.")
        return

    # Check if the file exists
    if not os.path.exists(file_path):
        print("File does not exist.")  # Debug: Log file existence check
        send_error(conn, 404, "File Not Found")
        return

    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        headers = build_response_headers(content_type, len(content))
        conn.sendall(headers + content)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # General exception logging
        send_error(conn, 500, "Internal Server Error")


# Get content type based on file extension
def get_content_type(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    print('file_extension', file_extension)
    if file_extension == '.html':
        return "text/html; charset=utf-8"
    elif file_extension == '.txt':
        return "text/plain; charset=utf-8"
    elif file_extension in ('.jpg', '.jpeg'):
        return "image/jpeg"
    elif file_extension == '.gif':
        return "image/gif"
    else:
        return None

# Builds HTTP response headers
def build_response_headers(content_type, content_length):
    current_time = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = f"HTTP/1.1 200 OK\r\n"
    headers += f"Date: {current_time}\r\n"
    headers += f"Content-Type: {content_type}\r\n"
    headers += f"Content-Length: {content_length}\r\n"
    headers += "\r\n"
    return headers.encode()

# Sends error messages to the client
def send_error(conn, status_code, message, extra_info=""):
    response = f"HTTP/1.1 {status_code} {message}\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    html_body = f"<html><head><title>{status_code} {message}</title></head><body><h1>{status_code} {message}</h1>{extra_info}</body></html>"
    response += f"Content-Length: {len(html_body)}\r\n"
    response += "Connection: close\r\n\r\n"
    response += html_body
    conn.sendall(response.encode('utf-8'))

listen()
