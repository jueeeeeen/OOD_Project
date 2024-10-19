import time
import psutil

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
        return f"{self.channel} {self.room_number}"
    
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
            print(f"Can't add {room_number}")
            
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
                print(f"Deleted room", end = " ")
                return root.right
            elif root.right is None:
                self.size -= 1
                print(f"Deleted room", end = " ")
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

    def inorder_sort(node, f):
        if node is not None:
            AVL.inorder_sort(node.left, f)
            f.write(node.show_room() + "\n")
            print(node.show_room())
            AVL.inorder_sort(node.right, f)
    
    def get_last_room(self):
        return AVL._get_last_room(self.root)
    
    def _get_last_room(node):
        if node.right is None:
            return node
        else:
            return AVL._get_last_room(node.right)
        
class Hotel:
    def __init__(self):
        self.AVL_hotel = AVL()

    # formula for calculating the room number for each guest
    def morton_curve(p, s, t, c, g):
        args = (p, s, t, c, g)
        max_bits = max(arg.bit_length() for arg in args)
        result = 0

        for i in range(max_bits):
            result |= ((p >> i) & 1) << (i * 5 + 0)
            result |= ((s >> i) & 1) << (i * 5 + 1)
            result |= ((t >> i) & 1) << (i * 5 + 2)
            result |= ((c >> i) & 1) << (i * 5 + 3)
            result |= ((g >> i) & 1) << (i * 5 + 4)

        return result
    
    # To measure runtime and memory usage in each function
    def runtime_and_memory(func):
        def wrapper(*args):
            start_time = time.time()
            process = psutil.Process()

            # Memory before execution
            mem_before = process.memory_info().rss
            process = psutil.Process()

            # Memory before execution
            mem_before = process.memory_info().rss
            result = func(*args)
            mem_after = process.memory_info().rss
            mem_after = process.memory_info().rss
            end_time = time.time()


            print(f"Runtime: {end_time - start_time:.5f} seconds")
            print(f"Memory usage: Before: {mem_before:.2f} Byte, After: {mem_after:.2f} Byte")
            print(f'Memory for this function: {mem_after - mem_before} Byte')
            return result
        return wrapper

    # sort the room number in AVL using inorder and write to file
    def write_to_file(self):
        with open("Hotel_Rooms", "w") as f:
            AVL.inorder_sort(self.AVL_hotel.root, f)
            
    # assign rooms for the guests from channels
    @runtime_and_memory
    def assign_rooms(self, plane, ship, train, car, guest):
        for g in range(guest):
            self.AVL_hotel.insert(Hotel.morton_curve(0, 0, 0, 0, g+1), f"old_no_{0}_{0}_{0}_{0}_{g+1}")
            
        total_rooms = plane * ship * train * car
        for i in range(total_rooms):
            p = (i // (ship * train * car)) % plane
            s = (i // (train * car)) % ship
            t = (i // (car)) % train
            c = (i) % car
            
            self.AVL_hotel.insert(Hotel.morton_curve(p, s, t, c, 0), f"no_{p+1}_{s+1}_{t+1}_{c+1}_{0}")
        
    # delete a room number manually    
    @runtime_and_memory 
    def delete_room(self, room_number):
        self.AVL_hotel.delete(room_number)
        print(room_number)

    # add a room number manually
    @runtime_and_memory  
    def add_room(self, room_number):
        self.AVL_hotel.insert(room_number, "manual")
    
    # search for a room number    
    @runtime_and_memory  
    def search_room(self, room_number):
        print(self.AVL_hotel.search(room_number))

    # show a number of the empty rooms
    @runtime_and_memory   
    def show_number_of_empty_room(self):
        print(f"Empty rooms : {self.AVL_hotel.get_last_room().room_number - self.AVL_hotel.size:,} rooms")
        
    # (additional) show a number of the reserved rooms (nodes in AVL)
    @runtime_and_memory
    def show_number_of_reserved_room(self):
        print(f"Reserved rooms : {self.AVL_hotel.size:,} rooms")
    
    # (additional) show last room number (biggest room number)
    @runtime_and_memory
    def show_last_room_number(self):
        print(f"last_room :\n{self.AVL_hotel.get_last_room().show_room()}")
        
hotel = Hotel()      
print("\n------------ Welcome to 404 Hotel Not Found ------------\n")
print("Please enter the number of guests in the hotel")

while True:
    try:
        guest = int(input("Guest : "))
        
        print("\nPlease enter the number of each travel channel (stack)")
        print("|    Plane    |    Ship    |    Train    |     Car     |")
        plane = int(input("Plane : "))
        ship = int(input("Ship  : "))
        train = int(input("Train : "))
        car = int(input("Car   : "))
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
    print("[f] show all rooms (sorted) in file")
    print("[l] show last room number")
    print("[q] exit")
    inp = input("Select mode : ")
    try:
        if inp == "e":
            print("--------------------------------------")
            hotel.show_number_of_empty_room()
        elif inp == "q":
            break
        elif inp == "r":
            print("--------------------------------------")
            hotel.show_number_of_reserved_room()
        elif inp == "f":
            print("--------------------------------------")
            hotel.write_to_file()
        elif inp == "l":
            hotel.show_last_room_number()
            print("--------------------------------------")
        elif inp[0] == "a":
            print(f"--------Adding room {inp[2:]}--------")
            hotel.add_room(int(inp[2:]))
        elif inp[0] == "d":
            print(f"-------Deleting room {inp[2:]}-------")
            hotel.delete_room(int(inp[2:]))
        elif inp[0] == "s":
            print(f"-------Searching room {inp[2:]}-------")
            hotel.search_room(int(inp[2:]))
    except:
        print("try again")
    print("-------------------------------------")