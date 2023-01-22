from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
import threading

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname()) # Get IP address of host computer name
ENCODING_DECODING_FORMAT: str = "utf-8"

COMMAND_SIZE: int = 2048 # Client and server can send and receive 2KB of data at a time

# Create socket that accepts IPv4 or IPv6 addresses and receives and transmits streams of data
server: socket = socket(AF_INET, SOCK_STREAM)

server.bind((HOST_IP, PORT))

def handle_client_connection(conn, addr):
    connected: bool = True

    while connected:
        client_command = conn.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)

        if str(client_command).lower == "exit":
            connected = False

        conn.sendall(client_command) # send command to all clients connected to server

    conn.close()

while True:
    print(f"Staring server....")
    print(f"Server listening on port: {PORT}")
    server.listen()
    client_conn, client_addr = server.accept() 
    client_thread = threading.Thread(target=handle_client_connection, args=(client_conn, client_addr))
    client_thread.start()