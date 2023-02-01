from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading, sys

from linked_list import LinkedList

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname()) # Get IP address of host computer name
ENCODING_DECODING_FORMAT: str = "utf-8"
COMMAND_SIZE: int = 2048 # Server can send and receive a maximum of 2KB of data at a time
NUM_OF_CLIENTS_SERVER_CAN_HANDLE: int = int(sys.argv[1])

client_list: LinkedList = LinkedList()

# Create socket that accepts IPv4 addresses and receives and transmits streams of data
server: socket = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server.bind((HOST_IP, PORT))
server.listen(NUM_OF_CLIENTS_SERVER_CAN_HANDLE)

print(f"Server listening on port: {PORT}")


def handle_client_connection(conn: socket, client_name: str):

    client_node: LinkedList.Node = LinkedList.Node(client_name, conn)
    client_list.insert_node(client_node)

    while True:
        try:
            client_command = conn.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)

            if client_command and client_command == "exit":
                conn.send(client_command.encode(ENCODING_DECODING_FORMAT))
                client_list.remove_node(client_name)
                break

            if client_command:
                client_list.broadcast_messages(client_command, client_name)

        except Exception as e:
            print(e.__str__)
            break

    conn.close()


def run() -> None:
    while True:
        client_conn, _ = server.accept() 
        client_name = client_conn.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT) # Receive one time client name
        client_thread = threading.Thread(target=handle_client_connection, args=(client_conn, client_name))
        client_thread.start()

run()