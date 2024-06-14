import binascii
import datetime
import string
import time
import sys

class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def add_node(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._add_node(value, self.root)

    def _add_node(self, value, current_node):
        if value < current_node.value:
            if current_node.left is None:
                current_node.left = TreeNode(value)
            else:
                self._add_node(value, current_node.left)
        elif value > current_node.value:
            if current_node.right is None:
                current_node.right = TreeNode(value)
            else:
                self._add_node(value, current_node.right)
        else:
            pass  # value already exists in the tree

    def search_node(self, value):
        return self._search_node(value, self.root)

    def _search_node(self, value, current_node):
        if current_node is None:
            return False
        elif current_node.value == value:
            return True
        elif value < current_node.value:
            return self._search_node(value, current_node.left)
        else:
            return self._search_node(value, current_node.right)
    
    def inorder_tree(self, current_node):
        if current_node is None:
            return []

        left = self.inorder_tree(current_node.left)
        right = self.inorder_tree(current_node.right)

        return left + [current_node.value] + right
    
    def get_depth(self):
        return self._get_depth(self.root)

    def _get_depth(self, current_node):
        if current_node is None:
            return 0

        left_depth = self._get_depth(current_node.left)
        right_depth = self._get_depth(current_node.right)

        return max(left_depth, right_depth) + 1



def load_hashes_from_file(file_path):
    with open(file_path, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        hashes = [h.split(':')[0] for h in hashes] # remove the ':' and the number that follows
        print(f"Loaded {len(hashes)} hashes from the file.")
        return hashes


def create_binary_search_tree(hashes):
    tree = BinarySearchTree()
    for h in hashes:
        hash_val_bytes = binascii.unhexlify(h)
        hash_val_int = int.from_bytes(hash_val_bytes, byteorder='little')
        tree.add_node(hash_val_int)
    print(f"Inserted {len(hashes)} elements into the tree.")
    return tree

def get_tree_size(tree):
    node_size = sys.getsizeof(tree.root) * len(tree.inorder_tree(tree.root))
    value_size = sys.getsizeof(tree.root.value) * len(tree.inorder_tree(tree.root))
    total_size = node_size + value_size
    return total_size


def get_decrypted_passwords(tree, file_path):
    decrypted_passwords = []

    with open(file_path, 'r') as f:
        for line in f:
            if ':' in line:
                decrypted_hash = line.split(':')[0].split('$')[-1].replace('NT', '').strip()
                if all(c in string.hexdigits for c in decrypted_hash):
                    hash_val_bytes = binascii.unhexlify(decrypted_hash)
                    hash_val_int = int.from_bytes(hash_val_bytes, byteorder='little')
                    if tree.search_node(hash_val_int):
                        decrypted_passwords.append(decrypted_hash)

    return decrypted_passwords
    
def compare_hashes(tree, original_hashes_path):
    original_hashes = load_hashes_from_file(original_hashes_path)
    false_positives = 0
    false_negatives = 0

    for original_hash in original_hashes:
        hash_val_bytes = binascii.unhexlify(original_hash)
        hash_val_int = int.from_bytes(hash_val_bytes, byteorder='little')
        if not tree.search_node(hash_val_int):
            false_positives += 1

    false_negatives = len(tree.inorder_tree(tree.root)) - (len(tree.inorder_tree(tree.root)) - false_positives)

    print("Comparison results:")
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

def main():
    hashes_path = 'original.txt'
    cracked_path = 'extended.txt'

    tree = create_binary_search_tree(load_hashes_from_file(hashes_path))

    search_start_time = time.perf_counter()
    print(f"Starting search at {datetime.datetime.now().strftime('%H:%M:%S')}")

    decrypted_passwords = get_decrypted_passwords(tree, cracked_path)

    search_end_time = time.perf_counter()
    search_time = search_end_time - search_start_time

    found_percentage = len(decrypted_passwords) / len(load_hashes_from_file(cracked_path)) * 100

    print(f"Process completed at {datetime.datetime.now().strftime('%H:%M:%S')}. We have found {found_percentage}% of hashes in the tree.")
    print(f"The search took {search_time:.9f} seconds.")

    compare_hashes(tree, hashes_path)
    
    # Calculate the size occupied by the tree in memory
    tree_depth = tree.get_depth()
    tree_size = sys.getsizeof(tree)


    # Obtain the variables/parameters that may influence the size of the tree
    variables_parameters = {
        'Number of nodes': len(tree.inorder_tree(tree.root)),
        'Size of stored values': sys.getsizeof(tree.root.value),
        'Tree depth': tree_depth
    }

    tree_size = get_tree_size(tree)
    print(f"Total tree size: {tree_size} bytes")

    print("Variables/parameters that may influence the size:")
    for variable, value in variables_parameters.items():
        print(f"{variable}: {value}")



if __name__ == '__main__':
    main()
