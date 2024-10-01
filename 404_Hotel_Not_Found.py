class Node:
    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left if left is not None else None
        self.right = right if right is not None else None
        self.height = 0
        
    def get_height(self, node):
        return -1 if node is None else node.height
        
    def set_height(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
    
    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)

class BST:
    def __init__(self):
        self.root = None
        
    def insert(self, data):
        self.root = BST._insert(self.root, data)
        
    def _insert(node, data):
        if node is None: return Node(data)
        if int(data) < int(node.data):
            node.left = BST._insert(node.left, data)
        else:
            node.right = BST._insert(node.right, data)
        return node
    
    def get_successor(node):
        cur = node.right
        while cur and cur.left:
            cur = cur.left
        return cur    
    
    def delete(self, data):
        self.root = BST._delete(self.root, data)
    
    def _delete(node, data):
        if node is None: return None
        if int(data) < int(node.data): node.left = BST._delete(node.left, data)
        elif int(data) > int(node.data): node.right = BST._delete(node.right, data)
        else:
            if node.left is None: return node.right
            elif node.right is None: return node.left
            new_root = BST.get_successor(node)
            node.data = new_root.data
            node.right = BST._delete(node.right, new_root.data)
        return node
    
    def print_tree(self):
        BST._print_tree(self.root)
        print()
        
    def _print_tree(node, level = 0):
        if node is not None:
            BST._print_tree(node.right, level+1)
            print('    '*level + node.data )
            BST._print_tree(node.left, level+1)
    
class AVL:
    def __init__(self):
        self.root = None
        
    def insert(self, data):
        self.root = AVL._insert(self.root, data)
    
    def _insert(node, data):
        if node is None:
            return Node(data)
        if int(data) < int(node.data):
            node.left = AVL._insert(node.left, data)
        elif int(data) > int(node.data):
            node.right = AVL._insert(node.right, data)
        else:
            return
            
        node.set_height()        
        new_root = AVL.rebalance(node)
        
        if new_root:
            return new_root
        return node
        
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
        
    def print_tree(self):
        AVL._print_tree(self.root)
        
    def _print_tree(node, level = 0):
        if node is not None:
            AVL._print_tree(node.right, level+1)
            print('    '*level + node.data )
            AVL._print_tree(node.left, level+1)
            
inp = input().split()
tree = BST()
for i in inp:
    tree.insert(i)
tree.print_tree()