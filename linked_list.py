class LinkedList:

    def __init__(self) -> None:
        self.head: LinkedList.Node = None
        self.total_rank: int = 0
    
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
            if node_to_be_removed.next == None:
                self.head = None
                del(node_to_be_removed)

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

        del(node_to_be_removed)

    
    def traverse_linked_list(self) -> None:
        current_node: LinkedList.Node = self.head

        while current_node != None:
            print(f"Name: {current_node.client_name}: Rank: {current_node.client_rank}")

            current_node = current_node.next

    def update_ranks(self) -> None:
        pass



if __name__ == "__main__":
    node_one = LinkedList.Node("Client one")
    node_two = LinkedList.Node("Client two")
    node_three = LinkedList.Node("Client three")
    node_four = LinkedList.Node("Client four")

    linked_list = LinkedList()

    linked_list.insert_node(node_one)
    linked_list.insert_node(node_two)
    linked_list.insert_node(node_three)
    linked_list.insert_node(node_four)

    linked_list.traverse_linked_list()

    print()

    linked_list.remove_node(1)

    linked_list.traverse_linked_list()