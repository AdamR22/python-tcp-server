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
    """
    Runs client for an indefinate amount of time.
    Program ends when user types exit in client or uses a keyboard interupt (ctrl + C)
    """

    while True:
        command = input(f"{CLIENT_NAME}$ ")
        client.send(command.encode(ENCODING_DECODING_FORMAT))

        # Commmand echoed by server from another client
        received_command: str = client.recv(COMMAND_SIZE).decode(ENCODING_DECODING_FORMAT)

        if not received_command or received_command != "exit":
            if not received_command:
                continue
            else:
                # shows if command comes from a senior or junior ranked server
                client_that_sent_command_class: str = received_command.split(":")[0].strip() 

                if client_that_sent_command_class == "Senior":
                    print("Executing command")
                    time.sleep(1) # Simulate pausing due to executing command
                    print("Command Executed.")
                    continue

                if client_that_sent_command_class == "Junior":
                    print("Cannot execute command from a lower ranked client.")
                    continue

                print(received_command)
        else:
            client.close()
            break
        
        
if __name__ == "__main__":
    run_client()