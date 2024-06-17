# Search Algorithms for Cracked NTLM Hashes

## General Description
This project evaluates the effectiveness of various search algorithms to identify NTLM hash matches in a dataset composed of previously filtered password hashes from cyber attacks. The data used comprises two main files: **original.txt** and **extended.txt**.

## Authors
This activity is part of the project R&D&I Laboratory on Cybersecurity, Privacy, and Secure Communications (TRUST Lab) financed by European Union NextGeneration-EU, the Recovery Plan, Transformation and Resilience,through INCIBE.

## Prerequisites

- Python: Version 3.11
- External libraries:
    - *cuckoofilter*: For Cuckoo filter implementation
    - *binascii*: For conversion between binary and ASCII

- Library installation: Use *pip* to install the necessary libraries. 

## Data Files

- **original.txt**: Contains unique NTLM password hashes an their occurrence frequency. 
- **extended.txt**: Includes NTLM hashes derived from a cracking process using John The Ripper, along with additional hashes not present in *original.txt*.

## Algorithms Implemented

- Linear Search
- Binary Search
- Hash Tables
- Binary Search Trees
- Cucko Filters

# Linear Search

## Configuration
No specific configuration is required. 

## Run the script:
> python linear_search.py

## Results
The results will be printed directly to the console, including the percentage of matches, false positives, and false negatives.

# Binary Search
## Configuration
No specific configuration is required.

## Run the script:
>python binary_search.py

## Results
The results will be printed directly to the console, including the match percentage and false positives.

# Hash Tables
## Configuration
No specific configuration is required.

## Run the script:
>python hash_table_search.py

## Results
The results will be printed directly to the console, including the match percentage, false positives, and the size of the hash table.

# Binary Search Trees
## Configuration
No specific configuration is required.

## Run the script:
>python binary_search_tree.py

## Results
The results will be printed directly to the console, including the match percentage, false positives, false negatives, and the tree's depth.

# Cuckoo Filters
## Configuration
- Capacity: Maximum number of elements the filter can store.
- Fingerprint Size: Size of the fingerprint in bits.
- Bucket Size: Number of fingerprints each bucket can store.

## Execution
Edit the script to adjust the capacity, fingerprint_size, and bucket_size variables if needed.

## Run the script:
>python cuckoo_filter.py

## Results
The results will be printed directly to the console, including the match percentage, false positives, false negatives, and the size of the Cuckoo filter.
