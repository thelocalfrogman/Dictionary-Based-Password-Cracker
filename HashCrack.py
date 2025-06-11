
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

print(input_list)

def checkHash(input_list):
    # Get the first item from the list
    first_input_hash = input_list[0]

    # Count the number of characters in the first item
    hashLength = len(first_input_hash)
    print(hashLength)

    if hashLength == 32:
        # MD5 Hash
        hash = "MD5"

    if hashLength == 40:
        # SHA1 Hash
        hash = "SHA1"

    if hashLength == 64:
        # SHA256 Hash
        hash = "SHA256"
        with open("./Testing/rockyou.txt", "r") as wordlist_file:
            wordlist_items = [line.strip() for line in wordlist_file]
            for items in wordlist_items:
                wordlist_hash = hashlib.md5(item.encode()).hexdigest() # Hashes wordlist item
                if wordlist_hash == target_hash:
                    print(f"Match found: {input_list}")
                else:
                    print("No match found") 

    if hashLength == 128:
      # SHA512 Hash
      hash = "SHA512"

checkHash(input_list)