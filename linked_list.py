class LinkedList:

    def __init__(self) -> None:
        self.head: LinkedList.Node = None
        self.total_rank: int = 0 # Helps in assigning rank to nodes/clients. Also shows total number of connected nodes/clients
    
    class Node:
        def __init__(self, client_name) -> None:
            self.client_name: int = client_name
            self.client_rank: int = 0
            self.prev: self = None
            self.next: self = None

    def insert_node(self, node: Node):
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

    def find_node_using_rank(self, rank: int) -> Node:
        if self.head.client_rank == rank:
            return self.head

        current_node: LinkedList.Node = self.head

        while current_node.client_rank != rank:
            current_node = current_node.next

        return current_node
    
    def remove_node(self, rank: int) -> None:
        node_to_be_removed: LinkedList.Node = self.find_node_using_rank(rank)

        if node_to_be_removed is self.head:
            # If client is the only one connected to server
            if node_to_be_removed.next == None:
                self.head = None
                del(node_to_be_removed)

            # If client was the first one to connect to server
            if node_to_be_removed.next != None:
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

    
    def traverse_linked_list(self) -> None:
        current_node: LinkedList.Node = self.head

        while current_node != None:
            print(f"Name: {current_node.client_name}: Rank: {current_node.client_rank}")

            current_node = current_node.next

    def update_ranks(self, node: Node) -> None:
        while node != None:
            node.client_rank -= 1
            node = node.next