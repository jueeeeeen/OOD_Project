import time
from memory_profiler import profile, memory_usage

class Room_Node:
    def __init__(self, room_number, channel, left = None, right = None):
        self.room_number = room_number
        self.channel = channel
        self.left = left if left is not None else None
        self.right = right if right is not None else None
        self.height = 0
        
    def __str__(self):
        return str(self.room_number)
    
    def show_room(self):
        return f"Room : {self.room_number}\nChannel : {self.channel}"
    
    def get_height(self, node):
        return -1 if node is None else node.height
        
    def set_height(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
    
    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)

class AVL:
    def __init__(self):
        self.root = None
        self.size = 0
        
    def insert(self, room_number, channel):
        self.root = self._insert(self.root, room_number, channel)
    
    def _insert(self, node, room_number, channel):
        if node is None:
            print(f"Added room {room_number}")
            self.size += 1
            return Room_Node(room_number, channel)
        if room_number < node.room_number:
            node.left = self._insert(node.left, room_number, channel)
        elif room_number > node.room_number:
            node.right = self._insert(node.right, room_number, channel)
        else:
            print(f"The room number {room_number} is reserved.")
            
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
    
    def get_successor(root):
        if root and root.left:
            return AVL.get_successor(root.left)
        else:
            return root
    
    def delete(self, data):
        self.root = self._delete(self.root, data)
        
    def _delete(self, root, room_number):
        if root is None: 
            print(f"Not found room", end=" ")
            return None
        if room_number < root.room_number: root.left = self._delete(root.left, room_number)
        elif room_number > root.room_number: root.right = self._delete(root.right, room_number)
        else:
            if root.left is None:
                self.size -= 1
                print(f"deleted room", end = " ")
                return root.right
            elif root.right is None:
                self.size -= 1
                print(f"deleted room", end = " ")
                return root.left
            new_root = AVL.get_successor(root.right)
            root.room_number = new_root.room_number
            root.right = self._delete(root.right, new_root.room_number)
        root.set_height()
        rebalanced_root = AVL.rebalance(root)
        return rebalanced_root if rebalanced_root else root
    
    def search(self, key):
        return AVL._search(self.root, key)
    
    def _search(root, key):
        if root is None: return f"Room {key} not found (empty)"
        if key == root.room_number: return root.show_room()
        if key < root.room_number: return AVL._search(root.left, key)
        return AVL._search(root.right, key)
        
    def print_tree(self):
        AVL._print_tree(self.root)
        
    def _print_tree(node, level = 0):
        if node is not None:
            AVL._print_tree(node.right, level+1)
            print('    '*level + str(node) )
            AVL._print_tree(node.left, level+1)

    def _inorder_sort(node, f):
        if node is not None:
            AVL._inorder_sort(node.left, f)
            f.write(node.show_room() + "\n\n")
            AVL._inorder_sort(node.right, f)
            
    def write_to_file(self):
        with open("Hotel_Rooms", "w") as f:
            AVL._inorder_sort(self.root, f)
    
    def get_last_room(self):
        return AVL._get_last_room(self.root)
    
    def _get_last_room(node):
        if node.right is None:
            return node.room_number
        else:
            return AVL._get_last_room(node.right)
        
    def runtime(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Runtime: {end_time - start_time:.5f} seconds")
            return result
        return wrapper
    
    @runtime
    @profile    
    def add_room(self, room_number):
        self.insert(room_number, "manual")
        self.write_to_file()
            
    @runtime
    @profile
    def assign_rooms(self, plane, ship, train, car, guest):
        for p in range(plane):
            for s in range(ship):
                for t in range(train):
                    for c in range(car):
                        for g in range(guest):
                            self.insert(AVL.morton_curve(p, s, t, c, g), f"no_{p+1}_{s+1}_{t+1}_{c+1}_{g+1}")
        self.write_to_file()
        self.show_number_of_reserved_room()
    
        
    @runtime
    @profile  
    def delete_room(self, room_number):
        self.delete(room_number)
        self.write_to_file()
    
    @runtime
    @profile    
    def search_room(self, room_number):
        print(self.search(room_number))
    
    @runtime
    @profile
    def show_number_of_reserved_room(self):
        print(f"Reserved rooms : {self.size:,} rooms")
    
    @runtime
    @profile    
    def show_number_of_empty_room(self):
        print(f"Empty rooms : {self.get_last_room() - self.size:,} rooms")
        
    def morton_curve(p, s, t, c, g):
        args = (p, s, t, c, g)
        result = 0
        for i in range(max(x.bit_length() for x in args)):
            for j, num in enumerate(args):
                result |= ((num >> i) & 1) << (i * len(args) + j)
        return result
        
class Hotel:
    def __init__(self):
        self.AVL_hotel = AVL()
        
hotel = AVL()                            
print("\n------------ Welcome to 404 Hotel Not Found ------------\n")
print("Please Enter a number of each traveling channel (stack)")
print("|   Plane   |   Ship   |   Train   |   Car   |  Guest  |")
while True:
    try:
        plane = int(input("Plane : "))
        ship = int(input("Ship  : "))
        train = int(input("Train : "))
        car = int(input("Car   : "))
        guest = int(input("Guest : "))
        break
    except ValueError:
        print("Invalid value please try again")
        print("--------------------------------------------------------")
print("--------------------------------------------------------")

hotel.assign_rooms(plane, ship, train, car, guest)

while True:
    print("[a] add <room number>")
    print("[d] delete <room number>")
    print("[s] search <room number>")
    print("[r] show number of reserved room")
    print("[e] show number of empty room")
    print("[q] exit")
    inp = input("Select mode : ")
    try:
        if inp == "e":
            print("--------------------------------------")
            start_time = time.time()
            hotel.show_number_of_empty_room()
            end_time = time.time()
            print(f"runtime: {end_time-start_time:.4f} seconds")
        elif inp == "q":
            break
        elif inp == "r":
            print("--------------------------------------")
            start_time = time.time()
            hotel.show_number_of_reserved_room()
            end_time = time.time()
            print(f"runtime: {end_time-start_time:.4f} seconds")
        elif inp[0] == "a":
            print(f"--------Adding room {inp[2:]}--------")
            start_time = time.time()
            hotel.add_room(int(inp[2:]))
            end_time = time.time()
            print(f"runtime: {end_time-start_time:.4f} seconds")
        elif inp[0] == "d":
            print(f"-------Deleting room {inp[2:]}-------")
            start_time = time.time()
            hotel.delete_room(int(inp[2:]))
            print(inp[2:])
            end_time = time.time()
            print(f"runtime: {end_time-start_time:.4f} seconds")
        elif inp[0] == "s":
            print(f"-------Searching room {inp[2:]}-------")
            start_time = time.time()
            hotel.search_room(int(inp[2:]))
            end_time = time.time()
            print(f"runtime: {end_time-start_time:.4f} seconds")
    except:
        print("try again")
    print("-------------------------------------")
