from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
import threading

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname()) # Get IP address of host computer name
ENCODING_DECODING_FORMAT: str = "utf-8"

# Create socket that accepts IPv4 or IPv6 addresses and receives and transmits streams of data
server: socket = socket(AF_INET, SOCK_STREAM)

server.bind((HOST_IP, PORT))

def handle_client_connection(conn, addr):
    pass

while True:
    print(f"Staring server....")
    print(f"Server listening on port: {PORT}")
    server.listen()
    client_conn, client_addr = server.accept() 
    client_thread = threading.Thread(target=handle_client_connection, args=(client_conn, client_addr))
    client_thread.start()