from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
import threading

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname()) # Get IP address of host computer name
ENCODING_DECODING_FORMAT: str = "utf-8"

COMMAND_SIZE: int = 2048 # Client and server can send and receive a maximum of 2KB of data at a time

# Create socket that accepts IPv4 addresses and receives and transmits streams of data
server: socket = socket(AF_INET, SOCK_STREAM)

server.bind((HOST_IP, PORT))
server.listen()
print(f"Server listening on port: {PORT}")

def handle_client_connection(conn):
    while True:
        client_command = conn.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)

        if client_command and client_command == "exit":
            conn.send(client_command.encode(ENCODING_DECODING_FORMAT))
            break

        if client_command:
            server.sendall(client_command.encode(ENCODING_DECODING_FORMAT))
            print(client_command)

    conn.close()

while True:
    client_conn, _ = server.accept() 
    client_thread = threading.Thread(target=handle_client_connection, args=(client_conn,))
    client_thread.start()