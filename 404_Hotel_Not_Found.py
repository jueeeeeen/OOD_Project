class Room_Node:
    def __init__(self, room_number, channel, left = None, right = None):
        self.room_number = room_number
        self.channel = {"plane": None, "ship": None, "train": None, "car": None}
        self.left = left if left is not None else None
        self.right = right if right is not None else None
        self.height = 0
        
    def __str__(self):
        return str(self.data)
        
    def get_height(self, node):
        return -1 if node is None else node.height
        
    def set_height(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
    
    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)

class AVL:
    def __init__(self):
        self.root = None
        
    def insert(self, room_number, channel):
        self.root = AVL._insert(self.root, room_number, channel)
    
    def _insert(node, room_number, channel):
        if node is None:
            return Room_Node(room_number, channel)
        if room_number < node.data:
            node.left = AVL._insert(node.left, room_number, channel)
        elif room_number > node.data:
            node.right = AVL._insert(node.right, room_number, channel)
        else:
            return
            
        node.set_height()        
        new_root = AVL.rebalance(node)
        
        return new_root if new_root else node
        
    def rebalance(node):
        balance = node.get_balance()
        if balance < -1:
            if node.right.get_balance() == 1:
                node.right = AVL.rotate_right(node.right)
            return AVL.rotate_left(node)
        elif balance > 1:
            if node.left.get_balance() == -1:
                node.left = AVL.rotate_left(node.left)
            return AVL.rotate_right(node)
        
    def get_successor(root):
        if root and root.left:
            AVL.get_successor(root.left)
        else:
            return root
        
    def rotate_left(root):
        new_root = root.right
        root.right = new_root.left
        new_root.left = root
        root.set_height()
        new_root.set_height()
        return new_root
    
    def rotate_right(root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
        root.set_height()
        new_root.set_height()
        return new_root
    
    def delete(self, data):
        self.root = AVL._delete(self.root, data)
        
    def _delete(root, data):
        if root is None: return None
        if data < root.data: root.left = AVL._delete(root.left, data)
        elif data > root.data: root.right = AVL._delete(root.right, data)
        else:
            if root.left is None: return root.right
            elif root.right is None: return root.left
            new_root = AVL.get_successor(root.right)
            root.data = new_root.data
            root.right = AVL._delete(root.right, new_root.data)
        root.set_height()
        new_root = AVL.rebalance(root)
        return new_root if new_root else root
    
    def search(self, key):
        return AVL._search(self.root, key)
    
    def _search(root, key):
        if root is None: return None
        if key == root.data: return str(root)
        if key < root.data: return AVL._search(root.left, key)
        return AVL._search(root.right, key)
        
    def print_tree(self):
        AVL._print_tree(self.root)
        
    def _print_tree(node, level = 0):
        if node is not None:
            AVL._print_tree(node.right, level+1)
            print('    '*level + str(node) )
            AVL._print_tree(node.left, level+1)
            
    def add_room(self, room_number):
        self.insert(room_number)
        
    def assign_rooms(self):
        plane = int(input("Enter number of plane : "))
        ship = int(input("Enter number of ship : "))
        train = int(input("Enter number of train : "))
        car = int(input("Enter number of car : "))
        passenger = int(input("Enter number of passenger : "))
        for p in range(plane):
            for s in range(ship):
                for t in range(train):
                    for c in range(car):
                        for person in range(passenger):
                            self.add_room((2**person) * (3**c) * (5**t) * (7**s) * (11**p))
    
    def show_room(self):
        self.print_tree()
        
    def delete_room(self, room_number):
        self.delete(room_number)
        
    def search_room(self, room_number):
        print(self.search(room_number))

hotel = AVL()                            
print("------- Welcome to 404 Not Found Hotel -------")
print("| Plane | Ship | Train | Car |")

hotel.assign_rooms()

while 1:
    inp = input("| del | add | search | show | exit |\ntype an action : ")
    if inp == "add":
        room_number = int(input("-----Adding a room-----\nEnter a room number : "))
        hotel.add_room(room_number)
    elif inp == "del":
        room_number = int(input("-----Deleting a room-----\nEnter a room number : "))
        hotel.delete_room(room_number)
    elif inp == "search":
        room_number = int(input("-----Searching a room-----\nEnter a room number : "))
        hotel.search_room(room_number)
    elif inp == "show":
        print("-----Showing rooms-----")
        hotel.show_room()
    elif inp == "exit":
        exit()
    else:
        print("try again")