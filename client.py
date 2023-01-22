from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname())
ENCODING_DECODING_FORMAT: str = "utf-8"

COMMAND_SIZE: int = 2048
client: socket = socket(AF_INET, SOCK_STREAM)
client.connect((HOST_IP, PORT))

while True:
    data = input("$ ")
    client.send(data.encode(ENCODING_DECODING_FORMAT))

    server_command = client.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)
    print(server_command)

    if not server_command or server_command != "exit":
        pass
    else:
        client.close()
        break