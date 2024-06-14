import sys
import time


def load_hashes_from_file(file_path):
    with open(file_path, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        hashes = [hash[4:].upper() if hash.startswith('$NT$') else hash.upper() for hash in hashes]
        print(f"Loaded {len(hashes)} hashes from the file.")
        return hashes


def create_binary_filter(hashes):
    sorted_hashes = sorted(hashes)
    print(f"Sorted {len(sorted_hashes)} hashes.")
    return sorted_hashes


def binary_search(clean_hashes, extended_hashes):
    sorted_clean_hashes = sorted(clean_hashes)
    found_hashes = []

    for extended_hash in extended_hashes:
        start = 0
        end = len(sorted_clean_hashes) - 1
        found = False

        while start <= end:
            middle = (start + end) // 2
            if sorted_clean_hashes[middle] == extended_hash:
                found = True
                break
            elif sorted_clean_hashes[middle] < extended_hash:
                start = middle + 1
            else:
                end = middle - 1

        if found:
            found_hashes.append(extended_hash)

    found_hashes_count = len(found_hashes)
    found_percentage = found_hashes_count / len(extended_hashes) * 100

    return found_hashes_count, found_percentage, found_hashes
    

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


def main():
    clean_file_path = 'original.txt'
    extended_file_path = 'extended.txt'
    clean_hashes = load_hashes_from_file(clean_file_path)
    extended_hashes = load_hashes_from_file(extended_file_path)

    # Create the binary filter
    binary_filter = create_binary_filter(clean_hashes)

    # Initial time measurement
    start_time = time.perf_counter()

    # Perform binary search and get the result
    search_result = binary_search(binary_filter, extended_hashes)
    found_hashes_count = search_result[0]
    found_percentage = search_result[1]
    found_hashes = search_result[2]

    # Final time measurement
    end_time = time.perf_counter()

    total_time = end_time - start_time
    formatted_time = format(total_time, ".6f")
    print(f"Percentage of found hashes: {found_percentage}%")
    print(f"Total search time: {formatted_time} s")

    # Compare hashes to obtain false positives and false negatives
    false_positives, false_negatives = compare_original_hashes(found_hashes, clean_hashes)
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    # Get the size of the binary filter
    binary_filter_size = sys.getsizeof(binary_filter)
    print(f"Binary filter size: {binary_filter_size} bytes")


if __name__ == '__main__':
    main()
