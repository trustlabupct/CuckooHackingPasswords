import time
import sys

def load_hashes_from_file(file_path):
    with open(file_path, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        print(f"Loaded {len(hashes)} hashes from the file.")
        return hashes

def load_decrypted_hashes_from_file(file_path):
    with open(file_path, 'r') as f:
        # Skip the first line of the file
        decrypted_hashes = []
        for line in f.readlines()[1:]:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                decrypted_hash = parts[0].upper().replace("$NT$", "")  # Convert to uppercase and remove "$NT$"
                decrypted_hashes.append(decrypted_hash)
        print(f"Loaded {len(decrypted_hashes)} decrypted hashes from the file.")
        return decrypted_hashes

def linear_search_hashes(hashes, decrypted_hashes):
    start_time = time.perf_counter()

    found_hashes = []
    for hash_orig in hashes:
        if hash_orig in decrypted_hashes:
            found_hashes.append(hash_orig)
    
    percentage_hashes = len(found_hashes) / len(decrypted_hashes) * 100

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Process starts at {time.strftime('%H:%M:%S')} on {time.strftime('%d/%m/%Y')}")
    print(f"Process ends at {time.strftime('%H:%M:%S')} on {time.strftime('%d/%m/%Y')}")
    print(f"Execution time: {elapsed_time:.9f} seconds")
    print(f"{percentage_hashes:.2f}% of hashes from cracked.txt found in hashes.txt")

    # Compare hashes to obtain false positives and false negatives
    false_positives = len(found_hashes) - len(hashes)
    false_negatives = len(hashes) - len(found_hashes)
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    # Get the size of the data structure
    data_structure_size = sys.getsizeof(hashes)
    print(f"Size of the data structure: {data_structure_size} bytes")


hashes_file_path = 'original.txt'
cracked_file_path = 'extended.txt'

hashes = load_hashes_from_file(hashes_file_path)
decrypted_hashes = load_decrypted_hashes_from_file(cracked_file_path)
linear_search_hashes(hashes, decrypted_hashes)
