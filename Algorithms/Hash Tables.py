import sys
import hashlib
import time


def load_hashes_from_file(file_path):
    with open(file_path, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        print(f"Loaded {len(hashes)} hashes from the file {file_path}.")
        return hashes


def create_hash_table(hashes):
    hash_table = {}
    for h in hashes:
        hash_table[h] = True
    print(f"Inserted {len(hash_table)} elements into the hash table.")
    return hash_table


def check_hashes_in_table(hash_table, hashes_to_check):
    found_hashes = []
    start_time = time.perf_counter()
    for h in hashes_to_check:
        if h in hash_table:
            found_hashes.append(h)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    percentage_found_hashes = len(found_hashes) / len(hashes_to_check) * 100
    print(f"Process completed at {time.strftime('%H:%M:%S')}. You have {percentage_found_hashes:.2f}% of hashes in the hash table. The comparison took {total_time:.9f} seconds.")
    return found_hashes


def compare_original_hashes(found_hashes, original_hashes):
    false_positives = 0
    false_negatives = 0

    for found_hash in found_hashes:
        if found_hash not in original_hashes:
            false_positives += 1

    for original_hash in original_hashes:
        if original_hash not in found_hashes:
            false_negatives += 1

    return false_positives, false_negatives


def get_data_structure_size(hash_table):
    size_in_bytes = sys.getsizeof(hash_table)
    return size_in_bytes


def main():
    hashes_file_path = 'original.txt'
    cracked_file_path = 'extended.txt'

    # Load hashes from hashes.txt and create hash table
    original_hashes = load_hashes_from_file(hashes_file_path)
    hash_table = create_hash_table(original_hashes)

    # Load hashes to check from cracked.txt
    hashes_to_check = []
    with open(cracked_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                decrypted_hash = parts[0][4:].upper()  # Remove the first 4 characters ($NT$) and convert to uppercase
                hashes_to_check.append(decrypted_hash)

    # Check hashes in hash table
    found_hashes = check_hashes_in_table(hash_table, hashes_to_check)

    # Compare hashes to obtain false positives and false negatives
    false_positives, false_negatives = compare_original_hashes(found_hashes, original_hashes)
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    # Get the size of the data structure
    hash_table_size = get_data_structure_size(hash_table)
    print(f"Size of the hash table: {hash_table_size} bytes")

    print("End of program")


if __name__ == '__main__':
    main()
