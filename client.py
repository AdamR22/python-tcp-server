from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
import string, random

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname())
ENCODING_DECODING_FORMAT: str = "utf-8"

COMMAND_SIZE: int = 2048

def random_string_generator() -> str:
    return ''.join(random.choice(string.ascii_letters) for i in range(10))

CLIENT_NAME: str = random_string_generator()

client: socket = socket(AF_INET, SOCK_STREAM)
client.connect((HOST_IP, PORT))

client.send(CLIENT_NAME.encode(ENCODING_DECODING_FORMAT))

while True:
    data = input(f"{CLIENT_NAME}$ ")
    client.send(data.encode(ENCODING_DECODING_FORMAT))

    server_command = client.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)
    print(server_command)

    if not server_command or server_command != "exit":
        pass
    else:
        client.close()
        break