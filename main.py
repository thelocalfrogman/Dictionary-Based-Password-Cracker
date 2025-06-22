# Authors:
#   William Chaston
#   George Ferres
# ---------------------------------
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

import os
import csv
import hashlib
from tqdm import tqdm
from pathlib import Path

file_path = 'a'
dic_path  = 'a'
hash_count = 0

def whathash(file_path): # Prompts the user to input the path to the file containing hashed passwords
    file_path = input("Please enter the hashes file path: ")

    path = Path(file_path)
    if path.exists():
        print(f"The file path '{file_path}' is valid.")
        file_name = file_path
        file_extension = Path(file_name).suffix
        print(f"The file extension is: {file_extension}")
        return file_path
    else:
        print(f"The file path '{file_path}' does not exist. Please check and try again.")
        whathash(file_path)

def whatdic(dic_path): # Prompts the user to input the path to the dictionary file
    dic_path = input("Please enter the dictionary file path: ")

    path = Path(dic_path)
    if path.exists():
        print(f"The file path '{dic_path}' is valid.")
        file_name = dic_path
        file_extension = Path(file_name).suffix
        print(f"The file extension is: {file_extension}")
        return dic_path
    else:
        print(f"The file path '{dic_path}' does not exist. Please check and try again.")
        whatdic(dic_path)

def detect_hash_type(hash_string): # Detects the type of a hash based on its character length
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

def try_variations(word, target_hash, hash_func, use_upper, use_lower, use_title): # Attempts to match various case variants of a word to a target hash
    attempts = [(word, 'original')] # Initialises the list of variations to try, starting with the plain attempt e.g 'password', 'original'
    if use_upper: # Check if use_upper is True from the beginning of the program
        attempts.append((word.upper(), 'upper')) # Each variation is added to the attempts list, with the identifier of what the variation is e.g 'PASSWORD', 'upper'
    if use_lower:
        attempts.append((word.lower(), 'lower'))
    if use_title:
        attempts.append((word.title(), 'title'))

    for variant, label in attempts:
        word_hash = hash_func(variant.encode()).hexdigest() # Hash variant
        if word_hash == target_hash: # Check variant against target hash
            return variant # Return the matching variant
    return None

def checkHashes(input_list, hash_count): # Compares each hash in the input list against words in the dictionary file
    for target_hash in tqdm(input_list, desc="Cracking hashes"): # Initialises progress bar
        print(f"\nChecking hash: {target_hash}")
        hash_func = detect_hash_type(target_hash)
        if not hash_func:
            print("Unknown hash type")
            continue

        # Reset variation flags for this hash
        use_upper = use_upper_input
        use_lower = use_lower_input
        use_title = use_title_input

        found = False

        # Open the dictionary file and iterate through each word
        with open(dic_path, "r", encoding="latin-1") as wordlist_file: # "latin-1" is needed because rockyou has non UTF-8 characters
            for line in wordlist_file:
                word = line.strip()
                match = try_variations(word, target_hash, hash_func,
                                       use_upper, use_lower, use_title)
                if match:
                    print(f"Match found: {match}")
                    hash_count += 1 # Keep track of number of cracked hashes
                    # Append the cracked pair to CSV
                    with open("cracked_hashes.csv", "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([target_hash, match])
                    found = True
                    break

        if not found:
            print("No match found.")
    return hash_count

# Prompt the user for file paths
file_path = whathash(file_path)
dic_path  = whatdic(dic_path)

# Prompt for variations to test
use_upper_input = input("Check UPPERCASE versions? (y/n): ").lower() == 'y' # "== 'y'" turn the answer into a boolean True/False statement
use_lower_input = input("Check lowercase versions? (y/n): ").lower() == 'y'
use_title_input = input("Check TitleCase versions? (y/n): ").lower() == 'y'

# Load hash list from the path entered by user
with open(file_path, "r") as input_file:
    input_list = [line.strip() for line in input_file]  # Gets each line of hash file

# Run the cracker
hash_count = checkHashes(input_list, hash_count)
print(f"Cracked Hashes: {hash_count}\nCracked Hash File: cracked_hashes.csv")
