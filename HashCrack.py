
# Feature: Converting input file to list and figure out what hash to use

import os
import hashlib

# hashlib.md5(b"password").hexdigest()
# hashlib.sha1(b"password").hexdigest()
# hashlib.sha256(b"password").hexdigest()
# hashlib.sha512(b"password").hexdigest()

hash = ""

with open("./Testing/input.txt", "r") as input_file:
    input_list = [line.strip() for line in input_file] # Gets each line of input file

def checkHash(input_list):
    target_hash = input_list[0]
    hashLength = len(target_hash) # Count the number of characters in the first item of input file
    print("Detected hash length:", hashLength)

    # Find hash based on length
    if hashLength == 32:
        hash_func = hashlib.md5
    elif hashLength == 40:
        hash_func = hashlib.sha1
    elif hashLength == 64:
        hash_func = hashlib.sha256
    elif hashLength == 128:
        hash_func = hashlib.sha512
    else:
        print("Unknown hash type.")
        return

    with open("./Testing/rockyou.txt", "r", encoding="latin-1") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            word_hash = hash_func(word.encode()).hexdigest() # Hashes wordlist item
            if word_hash == target_hash:
                print(f"Match found: {word}")
                return
        print("No match found.")

checkHash(input_list)