import cuckoofilter
import binascii
import time

def load_hashes_from_file(file_path):
    with open(file_path, 'r') as f:
        hashes = []
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                decrypted_hash = parts[0].upper()  # Convert to uppercase
                hashes.append(decrypted_hash)
        print(f"Loaded {len(hashes)} hashes from the file {file_path}.")
        return hashes


def create_cuckoo_filter(hashes, capacity, fingerprint_size):
    filter = cuckoofilter.CuckooFilter(capacity=capacity, fingerprint_size=fingerprint_size)
    for h in hashes:
        hash_val_bytes = binascii.unhexlify(h)
        filter.insert(hash_val_bytes)
    print(f"Inserted {filter.size()} elements into the filter.")
    return filter


def check_hashes_in_cuckoo_filter(filter, hashes_to_check):
    real_hash_count = 0
    found_hashes = []
    hashes_bytes = [binascii.unhexlify(h) for h in hashes_to_check]  # Pre-conversion to bytes
    start_time = time.perf_counter()
    for hash_val_bytes in hashes_bytes:
        if filter.contains(hash_val_bytes):
            real_hash_count += 1
            found_hashes.append(binascii.hexlify(hash_val_bytes).decode().upper())
    end_time = time.perf_counter()
    total_time = end_time - start_time
    percentage_in_filter = (real_hash_count / len(hashes_to_check)) * 100
    percentage_in_filter_str = f"{percentage_in_filter:.7f}".replace(".", ",")  # Replace dot with comma
    total_time_str = f"{total_time:.6f}".replace(".", ",")  # Replace dot with comma
    print(f"Percentage of real hashes in the cuckoo filter: {percentage_in_filter_str}%")
    print(f"Comparison time was {total_time_str} seconds.")
    return found_hashes

def calculate_false_positives(original_hashes, found_hashes):
    false_positive_count = 0
    true_positive_count = 0
    for h in found_hashes:
        if h not in original_hashes:
            false_positive_count += 1
        else:
            true_positive_count += 1

    print(f"Number of true positives: {true_positive_count}")
    print(f"Number of false positives: {false_positive_count}")
    print(f"Total number of found hashes: {len(found_hashes)}")


def main():
    hashes_file_path = 'original.txt'
    cracked_file_path = 'extended.txt'

    hashes = load_hashes_from_file(hashes_file_path)
    hashes_to_check = []

    with open(cracked_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                decrypted_hash = parts[0][4:].upper()  # Remove the first 4 characters ($NT$) and convert to uppercase
                hashes_to_check.append(decrypted_hash)

    capacities = [len(hashes) * i for i in range(1, 5)]
    fingerprint_sizes = [1, 2, 3, 4]

    for fingerprint_size in fingerprint_sizes:
        for capacity in capacities:
            filter = create_cuckoo_filter(hashes, capacity, fingerprint_size)
            print(f"Capacity: {capacity}, Fingerprint Size: {fingerprint_size}")
            found_hashes = check_hashes_in_cuckoo_filter(filter, hashes_to_check)
            calculate_false_positives(hashes, found_hashes)
            print()

    print("End of program")


if __name__ == '__main__':
    main()
