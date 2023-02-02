from socket import socket

class LinkedList:

    """
    Attributes
    - ENCODING_DECODING_FORMAT: Format for converting bytes to string
    - head: Inner class of type node
    - total_rank: number showing amount of clients connected to server. Also helps in assigning rank to client

    Description:
    A doubly linked list that temporarily stores clients connected to server.
    It acts as a pipeline, transmitting data received by the server from one client, to other clients.
    Responsible for assigning rank to clients when they connect to the server.
    Responsible for reassigning rank when appropriate to clients when one client disconnects.
    """


    def __init__(self) -> None:
        self.ENCODING_DECODING_FORMAT: str = "utf-8"
        self.head: LinkedList.Node = None
        self.total_rank: int = 0 # Helps in assigning rank to nodes/clients. Also shows total number of connected nodes/clients
    

    class Node:
        """
        Linked List inner class.

        Attributes:
        client_socket: Client connected to server
        client_name: Client generated username
        client_rank: Rank of client
        prev: Client elder ( Client that connected to server before current one )
        next: Client junior ( Client that connected to server after current one )

        Description:
        Serves as node to linked list and houses the client.
        """
        def __init__(self, client_name, client_socket: socket) -> None:
            self.client_socket: socket = client_socket
            self.client_name: int = client_name
            self.client_rank: int = 0
            self.prev: self = None
            self.next: self = None


    def insert_node(self, node: Node):

        """
        node: Inner class housing client connected to server

        Inserts client to linked list and assigns rank to client.
        """

        node.client_rank = self.total_rank

        self.total_rank += 1

        if not self.head: 
            self.head = node
            return

        current_node: LinkedList.Node = self.head

        while current_node.next != None:
            current_node = current_node.next
        
        current_node.next = node
        node.prev = current_node


    def find_node_using_name(self, name: str) -> Node:
        """
        name: Client generated username

        Finds node housing client in linked list using the client's generated username.
        """
        if self.head.client_name == name:
            return self.head

        current_node: LinkedList.Node = self.head

        while current_node.client_name != name:
            current_node = current_node.next

        return current_node


    def remove_node(self, name: str) -> None:
        """
        name: Client generated username

        Removes disconnected client from linked list and reassigns rank to remaining clients where appropriate.
        """

        node_to_be_removed: LinkedList.Node = self.find_node_using_name(name)

        if node_to_be_removed is self.head:
            # If client is the only one connected to server
            if node_to_be_removed.next == None:
                self.head = None
                del(node_to_be_removed)

            # If client was the first one to connect to server
            elif node_to_be_removed.next != None:
                self.update_ranks(node_to_be_removed)
                self.head = node_to_be_removed.next
                del(node_to_be_removed)

            return

        # If only one client is connected and that client disconnects
        if node_to_be_removed.next == None and node_to_be_removed.prev == None:
            self.head = None
            del(node_to_be_removed)
            return

        # If client is last client to be connected and that client disconnects
        if node_to_be_removed.next == None and node_to_be_removed.prev != None:
            prev_node: LinkedList.Node = node_to_be_removed.prev
            prev_node.next = None
            del(node_to_be_removed)
            return

        # If client is in the middle of the pack
        prev_node: LinkedList.Node = node_to_be_removed.prev
        next_node: LinkedList.Node = node_to_be_removed.next

        next_node.prev = prev_node
        prev_node.next = next_node

        self.update_ranks(next_node)

        del(node_to_be_removed)

        self.total_rank -= 1

    
    def broadcast_messages(self, command: str, client_name: str) -> None:
        """
        command: Prompt received by server from a client
        client_name: Name of client responsible for sending prompt/command

        Receives command from client and sends appropriate command to each client connected to server.
        Command sent to client depends on rank of client.
        """

        current_node: LinkedList.Node = self.head
        client_node: LinkedList.Node = self.find_node_using_name(client_name)

        while current_node != None:
            if current_node == client_node:
                current_node.client_socket.send(f"{command} command sent.".encode(self.ENCODING_DECODING_FORMAT))
            else:
                # Send command with tag showing it comes from a higher ranked client
                if current_node.client_rank > client_node.client_rank:
                    current_node.client_socket.send(f"Senior : {command}".encode(self.ENCODING_DECODING_FORMAT))

                # Send command with tag showing it comes from a lower ranked client
                if current_node.client_rank < client_node.client_rank:
                    current_node.client_socket.send(f"Junior : {command}".encode(self.ENCODING_DECODING_FORMAT))

            current_node = current_node.next


    def update_ranks(self, node: Node) -> None:
        """
        node: Position of client in linked list where ranks should begin being updated

        Updates client ranks where appropriate
        """
        while node != None:
            node.client_rank -= 1
            node = node.next