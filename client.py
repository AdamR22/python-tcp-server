from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
import string, random, time

PORT: int = 2781
HOST_IP: str = gethostbyname(gethostname())
ENCODING_DECODING_FORMAT: str = "utf-8"

COMMAND_SIZE: int = 2048 # Client able to send or receive commands that a <= 2KB in size


def random_string_generator() -> str:
    """
    Generates and returns random string that serves as client name
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(10))

CLIENT_NAME: str = random_string_generator()

client: socket = socket(AF_INET, SOCK_STREAM)
client.connect((HOST_IP, PORT))

client.send(CLIENT_NAME.encode(ENCODING_DECODING_FORMAT))


def run_client() -> None:
    while True:
        data = input(f"{CLIENT_NAME}$ ")
        client.send(data.encode(ENCODING_DECODING_FORMAT))

        # Commmand echoed by server from another client
        command_through_server: str = client.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)

        if not command_through_server or command_through_server != "exit":
            if not command_through_server:
                continue
            else:
                print(command_through_server)

                if "Executing" in command_through_server:
                    time.sleep(1) # Simulate executing command
                    print("Command executed")

                    continue 
        else:
            client.close()
            break
        
if __name__ == "__main__":
    run_client()