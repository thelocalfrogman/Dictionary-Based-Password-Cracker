import os
import csv
import hashlib
from tqdm import tqdm

hash_count = 0

use_upper_input = input("Check UPPERCASE versions? (y/n): ").lower()
use_lower_input = input("Check lowercase versions? (y/n): ").lower()
use_title_input = input("Check TitleCase versions? (y/n): ").lower()

with open("./Testing/Short/sha256_input_short.txt", "r") as input_file:
    input_list = [line.strip() for line in input_file] # Gets each line of input file
# Hash input files to test:
#   Long: (1500 Hashes)
#       - ./Testing/Long/md5_input.txt
#       - ./Testing/Long/sha1_input.txt
#       - ./Testing/Long/sha256_input.txt
#       - ./Testing/Long/sha512_input.txt
#   Short: (50 Hashes)
#       - ./Testing/Short/md5_input_short.txt
#       - ./Testing/Short/sha1_input_short.txt
#       - ./Testing/Short/sha256_input_short.txt
#       - ./Testing/Short/sha512_input_short.txt
#   Very Short: (5 Hashes)
#       - ./Testing/Very_Short/md5_input_very_short.txt
#       - ./Testing/Very_Short/sha1_input_very_short.txt
#       - ./Testing/Very_Short/sha256_input_very_short.txt
#       - ./Testing/Very_Short/sha512_input_very_short.txt

# Detect hash type based on character length
def detect_hash_type(hash_string):
    length = len(hash_string)
    if length == 32:
        return hashlib.md5
    elif length == 40:
        return hashlib.sha1
    elif length == 64:
        return hashlib.sha256
    elif length == 128:
        return hashlib.sha512
    else:
        return None

# Try matching word and variations
def try_variations(word, target_hash, hash_func, use_upper, use_lower, use_title):
    attempts = [(word, word)] # Initialises the list of variations to try, starting with the plain attempt e.g 'password', 'password'
    if use_upper == True:
        attempts.append((word.upper(), 'upper')) # Each variation is added to the attempts list, with the identifyer of what the variation is e.g 'PASSWORD', 'upper'
    if use_lower == True:
        attempts.append((word.lower(), 'lower'))
    if use_title == True:
        attempts.append((word.title(), 'title'))

    for variant, label in attempts: # Looping through the attempts list containing the variations
        word_hash = hash_func(variant.encode()).hexdigest()
        if word_hash == target_hash:
            return variant  # Return the matching variant
    return None


def checkHashes(input_list, hash_count):
    for target_hash in tqdm(input_list, desc="Cracking hashes"): # Initialises progress bar, though the hashes crack so quickly you can't tell
        print(f"\nChecking hash: {target_hash}")
        hash_func = detect_hash_type(target_hash) # Find hash type
        if not hash_func:
            print("Unknown hash type")
            continue

        # Reset variation flags for this hash
        use_upper = use_upper_input
        use_lower = use_lower_input
        use_title = use_title_input

        found = False

        with open("./Testing/rockyou.txt", "r", encoding="latin-1") as wordlist_file: # "latin-1" is needed because rockyou has non UTF-8 characters
            for line in wordlist_file:
                word = line.strip()
                match = try_variations(word, target_hash, hash_func, use_upper, use_lower, use_title)
                if match:
                    print(f"Match found: {match}")
                    hash_count = hash_count + 1
                    with open("cracked_hashes.csv", "a", newline="") as csvfile: # Append hash and plaintext password to CSV file
                        writer = csv.writer(csvfile)
                        writer.writerow([target_hash, match])
                    found = True
                    break

        if not found:
            print("No match found.")
    return hash_count

hash_count = checkHashes(input_list, hash_count)
print(f"Cracked Hashes: {hash_count}\nCracked Hash File: cracked_hashes.csv")